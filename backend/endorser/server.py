from flask import Flask, jsonify, request
import atexit
import os
from indy import pool, wallet, did, ledger, blob_storage,anoncreds
import json
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求


def run_async(coroutine):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)

def shutdown():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if endorser['pool'] is not None:
        run_async(pool.close_pool_ledger(endorser['pool']))
    if endorser['wallet'] is not None:
        print("Closing wallet...")
        run_async(wallet.close_wallet(endorser['wallet']))
    loop.close()

atexit.register(shutdown)

endorser = {
      'name': "Endorser",
      'wallet_config': None,
      'wallet_credentials': None,
    #   'wallet_config': json.dumps({'id': 'sovrin_endorser_wallet'}),
    #   'wallet_credentials': json.dumps({'key': 'endorser_wallet_key'}),
      'pool': None,
      'seed': None,
      'wallet': None,
  }

async def initialize_pool():
    # pool_config = json.dumps({"genesis_txn": "/root/citi/poolfile"})
    # await pool.create_pool_ledger_config("testpool", pool_config)
    pool_handle = await pool.open_pool_ledger("testpool", None)
    endorser['pool'] = pool_handle
    return pool_handle

async def initialize_wallet(wallet_name:str, wallet_key:str):
    # Create wallet
    endorser['wallet_config'] = json.dumps({'id': wallet_name})
    endorser['wallet_credentials'] = json.dumps({'key': wallet_key})
    await wallet.create_wallet(endorser['wallet_config'], endorser['wallet_credentials'])
    # wallet.create_wallet(endorser['wallet_config'], endorser['wallet_credentials'])
    endorser['wallet'] = await wallet.open_wallet(endorser['wallet_config'], endorser['wallet_credentials'])

async def create_did(wallet_handle, seed=None):
    if seed is None:
        (endorser['did'], endorser['verkey']) = await did.create_and_store_my_did(wallet_handle, json.dumps({"seed": endorser['seed']}))
    else:
        (endorser['did'], endorser['verkey']) = await did.create_and_store_my_did(wallet_handle, json.dumps({"seed": seed}))
    return endorser['did'], endorser['verkey']
    

@app.route("/api/create_wallet", methods=["POST"])
def api_create_wallet():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    wallet_key = data.get("wallet_key")
    if not wallet_name or not wallet_key:
        return jsonify({"status": "error", "message": "Missing required fields"})
    res=run_async(initialize_wallet(wallet_name, wallet_key))
    return jsonify({"status": "success", "message": res})
    
@app.route("/api/open_wallet", methods=["POST"])
def api_open_wallet():
    if(endorser['wallet'] != None):
        run_async(wallet.close_wallet(endorser['wallet']))
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    wallet_key = data.get("wallet_key")
    endorser['walletname'] = wallet_name
    if not wallet_name or not wallet_key:
        return jsonify({"status": "error", "message": "Missing required fields"})
    endorser["wallet"] = run_async(wallet.open_wallet(json.dumps({'id': wallet_name}), json.dumps({'key': wallet_key})))
    return jsonify({"status": "success", "message": None})

@app.route("/api/create_did", methods=["POST"])
def api_create_did():
    if(endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    seed = data.get("seed")
    if not seed:
        return jsonify({"status": "error", "message": "Missing required fields"})
    res = run_async(create_did(endorser['wallet'], seed))
    return jsonify({"status": "success", "message": res})
    
@app.route("/api/list_did", methods=["GET"])
def api_list_did():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    res= run_async(did.list_my_dids_with_meta(endorser['wallet']))
    return jsonify({"status": "success", "message": res})


@app.route("/api/create_user", methods=["POST"])
def api_create_user():
    data = request.get_json()
    mydid = data.get("mydid")
    newdid = data.get("newdid")
    newverkey = data.get("newverkey")
    role = data.get("role")
    if not mydid or not newdid or not newverkey :
        return jsonify({"status": "error", "message": "Missing required fields"})
    nym_request = run_async(ledger.build_nym_request(mydid, newdid, newverkey, None, role))
    res = run_async(ledger.sign_and_submit_request(endorser['pool'], endorser['wallet'], mydid, nym_request))
    return jsonify({"status": "success", "message": res})

@app.route("/api/create_schema", methods=["POST"])
def api_create_schema():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    schema_name = data.get("schema_name")
    schema_version = data.get("version")
    schema_attrs = data.get("attributes")
    mydid= data.get("mydid")
    if not schema_name or not schema_version or not schema_attrs:
        return jsonify({"status": "error", "message": "Missing required fields"})
    schema_id, schema_json = run_async(anoncreds.issuer_create_schema(mydid, schema_name, schema_version, json.dumps(schema_attrs)))
    schema_request = run_async(ledger.build_schema_request(mydid, schema_json))
    
    

    res = run_async(ledger.sign_and_submit_request(endorser['pool'], endorser['wallet'], mydid, schema_request))
    
    
    # Parse the response to extract seqNo
    res_json = json.loads(res)
    seq_no = res_json.get("result", {}).get("txnMetadata", {}).get("seqNo")


    # Ensure the directory exists
    directory = f"../saves/endorser/{endorser['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Add seqNo to schema_json
    schema_json = json.loads(schema_json)
    schema_json["seqNo"] = seq_no
    schema_json = json.dumps(schema_json)

    # Save updated schema json into database
    with open(f"{directory}/schemas.json", "a") as schema_file:
        schema_file.write(schema_json + "\n")
    
    
    return jsonify({"status": "success", "message": res})

@app.route("/api/list_schema", methods=["GET"])
def api_list_schema():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    
    with open(f"../saves/endorser/{endorser['walletname']}/schemas.json", "r") as schema_file:
        schemas = schema_file.readlines()
    schemas = [schema.strip() for schema in schemas]
    return jsonify({"status": "success", "message": schemas})

@app.route("/api/create_cred_def", methods=["POST"])
def api_create_cred_def():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    schema = data.get("schema")
    tag = data.get("tag")
    mydid= data.get("mydid")
    config= data.get("config")
    type = data.get("type")
    if type is None:
        type = "CL"
    if config is None:
        config = {"support_revocation": False}
    if not schema or not tag:
        return jsonify({"status": "error", "message": "Missing required fields"})

    schema_json = json.dumps(schema)
    cred_def_id, cred_def_json = run_async(anoncreds.issuer_create_and_store_credential_def(endorser['wallet'], mydid, schema_json, tag, type, json.dumps(config)))
    
    

    cred_def_request = run_async(ledger.build_cred_def_request(mydid, cred_def_json))
    res = run_async(ledger.sign_and_submit_request(endorser['pool'], endorser['wallet'], mydid, cred_def_request))
    
    # please save cred def json into database
    # Ensure the directory exists
    directory = f"../saves/endorser/{endorser['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/cred_defs.json", "a") as cred_def_file:
        cred_def_file.write(cred_def_json + "\n")
    
    return jsonify({"status": "success", "message": res})

@app.route("/api/list_cred_def", methods=["GET"])
def api_list_cred_def():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    
    with open(f"../saves/endorser/{endorser['walletname']}/cred_defs.json", "r") as cred_def_file:
        cred_defs = cred_def_file.readlines()
    cred_defs = [cred_def.strip() for cred_def in cred_defs]
    return jsonify({"status": "success", "message": cred_defs})

@app.route("/api/create_credential_offer", methods=["POST"])
def api_create_credential_offer():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    cred_def_id = data.get("cred_def_id")
    if not cred_def_id:
        return jsonify({"status": "error", "message": "Missing required fields"})
    cred_offer = run_async(anoncreds.issuer_create_credential_offer(endorser['wallet'], cred_def_id))

    # please save cred offer into database
    # Ensure the directory exists
    directory = f"../saves/endorser/{endorser['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/cred_offer.json", "a") as cred_offer_file:
        cred_offer_file.write(cred_offer + "\n")

    return jsonify({"status": "success", "message": cred_offer})

@app.route("/api/list_cred_offer", methods=["GET"])
def api_list_cred_offer():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    
    with open(f"../saves/endorser/{endorser['walletname']}/cred_offer.json", "r") as cred_offer_file:
        cred_offers = cred_offer_file.readlines()
    cred_offers = [cred_offer.strip() for cred_offer in cred_offers]
    return jsonify({"status": "success", "message": cred_offers})

# # Faber Agent
  # note that encoding is not standardized by Indy except that 32-bit integers are encoded as themselves. IS-786
#   transcript_cred_values = json.dumps({
#       "first_name": {"raw": "Alice", "encoded": "1139481716457488690172217916278103335"},
#       "last_name": {"raw": "Garcia", "encoded": "5321642780241790123587902456789123452"},
#       "degree": {"raw": "Bachelor of Science, Marketing", "encoded": "12434523576212321"},
#       "status": {"raw": "graduated", "encoded": "2213454313412354"},
#       "ssn": {"raw": "123-45-6789", "encoded": "3124141231422543541"},
#       "year": {"raw": "2015", "encoded": "2015"},
#       "average": {"raw": "5", "encoded": "5"}
#   })

@app.route("/api/create_credential", methods=["POST"])
def api_create_credential():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    cred_offer = json.dumps(data.get("cred_offer"))
    cred_request = json.dumps(data.get("cred_request"))
    cred_values = json.dumps(data.get("cred_values"))
    # cred_offer = json.dumps({"schema_id":"STdrURQUU64d3JDUNbrc2T:2:PersonalAssets:1.0","cred_def_id":"STdrURQUU64d3JDUNbrc2T:3:CL:29:tag1","key_correctness_proof":{"c":"84188786964457146177006710943936901122517459630246581709705963596213374860065","xz_cap":"1460301421478817695234074216037785647603093203820262176645844387992551958405870603493110483185564770663456049328310956983321709551493421400851613173552162627868862028669120152315106027059819653845990645815318509593424131754479177495355719790791842377961190646599614710440678592032444557092304413756288695245368056298981421651420955843808868969081058663964506719257225966012312739111114546347560282217962207818031775319337320327968718221552178937225421417071970273601763165816598419359191845895075559081574098334779195435959410791728620151757083311779568733735270883739184405320147510632279310917390299912623340176490375965324431094493381056276015846862613182847880832320682605200138555625480373","xr_cap":[["balance","1012921201976488699020354495049929259718057058323465119776252177489230873350478880673310554591940414421272051519284504182346503496818994427763838851024818230919905838349437983277756504169537299537140391688243358884719921349797503425280489906404879224426607021043800477862347476971960739566102561233447923069258233259707514903849319598287377698184187388883812432719376290395844942688703799919378888687317511939908683415231131168217047695279568030823485583263706764735439424687175139225366192178889953638091683224728718590233126936956999083912967272423378332033254444551282624732159630138277122857222914554631943499054928679900899695293829711321278004157933062471854035660489904811112121808766290"],["master_secret","1983837118850496798717962835602072214292184909007448516016414319047991298290508585921680057494037521650879295593150652688578691203144025778816399944791320895095775720302647623363425805581891267483760521347705151634537232396308904675294334173668610249013420047341949730209233333187169362953275601503319678600712003011603593691247699614133467637962985142160291603130361401121617631115614052457785754823035032636625062479634659118805418543113968372725302723326695686890337860814222029220986779790671947388132362434988027433253582574868808987797612074217626357286380678953721514187684237919760940050216316217721008569685884239765803588624678145641287300879681871261265964247858876149426722599154833"],["credit","1740362684675420113124708741510293466827826548718351319405764397027503118776725662461573468129485390795080438037455182820076455685925270236849740844464821571402361255650927814271170824133565623637124648418438887125618891075138385267602128891239348998870333830073056060846607950675036834978210747520550823515347328384982501233993338419638664103024775887269810522560724130138594996160204789610425139254995759214046432072501417046443110015622793345965317658116009312839296795345792693682180620863416862209720092447293132340732001618020937502721974438297014110124756206069097000546135634850667717168841709698004051563732745659751498688640775056212583695498526863283348908379773324087720456827698752"],["age","1574386579210092970839442076755857849871514758883254058005619209283833013423480487896896897811338885776497738764952046319573682890240450596432014843452038894822371961291895819994904792821602538554626042597044821353371972796600612002797456584594118924587773161079826436495252992041983804958069782662352407572513151820622461207379369254679054926526385477923610138998067049454577091855258192395995585313253684989353551144099867295505330464262748551909591505792509852130166312816556668274758234054737292979261807216818637335010364226831075783994029907464209493041756372078152464722109774369377376839449768597744881357223791521628359144703477975909870290338294331905648066481964475816195531237453630"],["name","1420428725266283621233380528125471634210035325201073220247417015372642069461662561591858682717489378827373271187453099655236845270862855587377479994466009578181833715213488073647302730802946695507607678121009715637068765629599159194652683540320048568723601306654547637856124796458234842770295383937756422071459720096423767995273403368482734325518042550335572730581153934586921790113263421978658687875725619835913447403157610954109088105782092838618172763853256771878822936698761475212555145536677436092003823769684010402732914004845139716685159408576079880838655924384966412648740504613662788859408643390709432256888592738114579720799330845074846145169400121879795394037398760458211443175926163"]]},"nonce":"971897207750564866453581"})
    # cred_request = json.dumps(json.loads('{"prover_did":"VdUVTew6fFmWMXZPyTfqp1","cred_def_id":"STdrURQUU64d3JDUNbrc2T:3:CL:29:tag1","blinded_ms":{"u":"14411092805427477977079933957926195816059211834970609745689584259240260524592555462634506632022590768642014901968047467630774311836185147293380254265225401582257566786690857995881339190742212602885362516840167179905775828346312280985138330931786301017917214310195645304778750163317360784153497263409640040201582232693823066195900633069673389893394289113986605432836458155903274269813666980641123733506847084831951949365776196941618182342712678753389960760478562757250121868503757625519504554134298079364732208270175179319034162924110552163488024646483416818564516798296492505076511680903732964230792890613966446950081","ur":null,"hidden_attributes":["master_secret"],"committed_attributes":{}},"blinded_ms_correctness_proof":{"c":"74874479647935557207924550073654361841579825571887764286957345438526879457500","v_dash_cap":"310489779063226456553130226994468484192077236905810608019558256455315826409283595663042363456681521518709460926925615869301217520780104825410440583908172135811910831952414240899407327641300033925846873853245353324060745811213771744018079066049880667147069982539903372838620647719887561134740244422014013660374426828256611889294413997642372664854931110176859383854910853219635587769838671858474394716886494170164027014358176184752556901396031804992387093512572697390441707031622875006852589738760408644405677099954699465421520849557583716274625436451426983775236315454535267305970437287154129621464461805481466012999326618662197691924195222311156054506224379333529450990458901848419825499183939786618602271698227065427","m_caps":{"master_secret":"22815299991295377540107557420785338722605193591376775643217078314211578559010513929209187554717340929047317434531929270803335055955816826665983878090337531736404161516804770525417"},"r_caps":{}},"nonce":"752276803333231278276571"}'))
    # cred_values = json.dumps({ "name": {"raw": "GodricLee", "encoded": "1139481716457488690172217916278103335"}, "age": {"raw": "20", "encoded": "20"}, "balance": {"raw": "200000", "encoded": "200000"}, "credit": {"raw": "High", "encoded": "235325346346456346435345"}, })
    if not cred_offer or not cred_request or not cred_values:
        return jsonify({"status": "error", "message": "Missing required fields"})
    cred_json,_,_ = run_async(anoncreds.issuer_create_credential(endorser['wallet'], cred_offer, cred_request, cred_values, None, None))
    
    # please save cred json into database
    # Ensure the directory exists
    directory = f"../saves/endorser/{endorser['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/cred_json.json", "a") as cred_json_file:
        cred_json_file.write(cred_json + "\n")

    return jsonify({"status": "success", "message": cred_json})

@app.route("/api/list_cred", methods=["GET"])
def api_list_cred():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    
    with open(f"../saves/endorser/{endorser['walletname']}/cred_json.json", "r") as cred_json_file:
        creds = cred_json_file.readlines()
    creds = [cred.strip() for cred in creds]
    return jsonify({"status": "success", "message": creds})

@app.route("/api/verify_proof", methods=["POST"])
def api_verify_proof():
    if (endorser['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    proof_req = json.dumps(data.get("proof_req"))
    proof = json.dumps(data.get("proof"))
    schema = json.dumps(data.get("schema"))
    cred_def = json.dumps(data.get("cred_def"))
    if not proof_req or not proof:
        return jsonify({"status": "error", "message": "Missing required fields"})
    
    res = run_async(anoncreds.verifier_verify_proof(proof_req, proof, schema, cred_def, "{}","{}"))
    
    return jsonify({"status": "success", "message": res})

if __name__ == "__main__":
    print("Initializing pool...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_pool())
    loop.close()
    app.run(host="0.0.0.0", port=5002, debug=1)
