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
    if user['pool'] is not None:
        run_async(pool.close_pool_ledger(user['pool']))
    if user['wallet'] is not None:
        print("Closing wallet...")
        run_async(wallet.close_wallet(user['wallet']))
    loop.close()

atexit.register(shutdown)

user = {
      'name': "user",
      'wallet_config': None,
      'wallet_credentials': None,
    #   'wallet_config': json.dumps({'id': 'sovrin_user_wallet'}),
    #   'wallet_credentials': json.dumps({'key': 'user_wallet_key'}),
      'pool': None,
      'seed': None,
      'wallet': None,
      'master_secret': None,
  }

async def initialize_pool():
    # pool_config = json.dumps({"genesis_txn": "/root/citi/poolfile"})
    # await pool.create_pool_ledger_config("testpool", pool_config)
    pool_handle = await pool.open_pool_ledger("testpool", None)
    user['pool'] = pool_handle
    return pool_handle

async def initialize_wallet(wallet_name:str, wallet_key:str):
    # Create wallet
    user['wallet_config'] = json.dumps({'id': wallet_name})
    user['wallet_credentials'] = json.dumps({'key': wallet_key})

    # await wallet.delete_wallet(user['wallet_config'], user['wallet_credentials'])

    await wallet.create_wallet(user['wallet_config'], user['wallet_credentials'])
    user['wallet'] = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials'])

    user['master_secret'] =  await anoncreds.prover_create_master_secret(user['wallet'], None)
    user['walletname']= wallet_name
    directory = f"../saves/user/{user['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/master_secret.json", "a") as master_secret_file:
        master_secret_file.write(user['master_secret'] + "\n")

async def create_did(wallet_handle, seed=None):
    if seed is None:
        (user['did'], user['verkey']) = await did.create_and_store_my_did(wallet_handle, json.dumps({"seed": user['seed']}))
    else:
        (user['did'], user['verkey']) = await did.create_and_store_my_did(wallet_handle, json.dumps({"seed": seed}))
    return user['did'], user['verkey']
    

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
    if(user['wallet'] != None):
        run_async(wallet.close_wallet(user['wallet']))
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    wallet_key = data.get("wallet_key")
    user['walletname'] = wallet_name
    if not wallet_name or not wallet_key:
        return jsonify({"status": "error", "message": "Missing required fields"})
    user["wallet"] = run_async(wallet.open_wallet(json.dumps({'id': wallet_name}), json.dumps({'key': wallet_key})))
    return jsonify({"status": "success", "message": None})

@app.route("/api/create_did", methods=["POST"])
def api_create_did():
    if(user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    seed = data.get("seed")
    if not seed:
        return jsonify({"status": "error", "message": "Missing required fields"})
    res = run_async(create_did(user['wallet'], seed))
    return jsonify({"status": "success", "message": res})
    
@app.route("/api/list_did", methods=["GET"])
def api_list_did():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    res= run_async(did.list_my_dids_with_meta(user['wallet']))
    return jsonify({"status": "success", "message": res})


@app.route("/api/create_user", methods=["POST"])
def api_create_user():
    data = request.get_json()
    mydid = data.get("mydid")
    newdid = data.get("newdid")
    newverkey = data.get("newverkey")
    role = data.get("role")
    if not mydid or not newdid or not newverkey or not role:
        return jsonify({"status": "error", "message": "Missing required fields"})
    nym_request = run_async(ledger.build_nym_request(mydid, newdid, newverkey, None, role))
    res = run_async(ledger.sign_and_submit_request(user['pool'], user['wallet'], mydid, nym_request))
    return jsonify({"status": "success", "message": res})

@app.route("/api/create_schema", methods=["POST"])
def api_create_schema():
    if (user['wallet'] == None):
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
    
    

    res = run_async(ledger.sign_and_submit_request(user['pool'], user['wallet'], mydid, schema_request))
    
    
    # Parse the response to extract seqNo
    res_json = json.loads(res)
    seq_no = res_json.get("result", {}).get("txnMetadata", {}).get("seqNo")


    # Ensure the directory exists
    directory = f"../saves/user/{user['walletname']}"
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
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    mydid = data.get("mydid")
    if not mydid:
        return jsonify({"status": "error", "message": "Missing required fields"})
    with open(f"../saves/user/{user['walletname']}/schemas.json", "r") as schema_file:
        schemas = schema_file.readlines()
    schemas = [schema.strip() for schema in schemas]
    return jsonify({"status": "success", "message": schemas})

@app.route("/api/create_cred_def", methods=["POST"])
def api_create_cred_def():
    if (user['wallet'] == None):
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
    cred_def_id, cred_def_json = run_async(anoncreds.issuer_create_and_store_credential_def(user['wallet'], mydid, schema_json, tag, type, json.dumps(config)))
    
    

    cred_def_request = run_async(ledger.build_cred_def_request(mydid, cred_def_json))
    res = run_async(ledger.sign_and_submit_request(user['pool'], user['wallet'], mydid, cred_def_request))
    
    # please save cred def json into database
    # Ensure the directory exists
    directory = f"../saves/user/{user['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/cred_defs.json", "a") as cred_def_file:
        cred_def_file.write(cred_def_json + "\n")
    
    return jsonify({"status": "success", "message": res})

@app.route("/api/list_cred_def", methods=["GET"])
def api_list_cred_def():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    mydid = data.get("mydid")
    if not mydid:
        return jsonify({"status": "error", "message": "Missing required fields"})
    with open(f"../saves/user/{user['walletname']}/cred_defs.json", "r") as cred_def_file:
        cred_defs = cred_def_file.readlines()
    cred_defs = [cred_def.strip() for cred_def in cred_defs]
    return jsonify({"status": "success", "message": cred_defs})

@app.route("/api/create_credential_offer", methods=["POST"])
def api_create_credential_offer():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    cred_def_id = data.get("cred_def_id")
    if not cred_def_id:
        return jsonify({"status": "error", "message": "Missing required fields"})
    cred_offer = run_async(anoncreds.issuer_create_credential_offer(user['wallet'], cred_def_id))
    return jsonify({"status": "success", "message": cred_offer})

@app.route("/api/create_master_secret", methods=["POST"])
def api_create_master_secret():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()

    user['master_secret'] = run_async( anoncreds.prover_create_master_secret(user['wallet'], user['walletname']))

    #please save it to database
    # Ensure the directory exists
    directory = f"../saves/user/{user['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/master_secret.json", "a") as master_secret_file:
        master_secret_file.write(user['master_secret'] + "\n")
    # print(user['master_secret'])

    return jsonify({"status": "success", "message": user['master_secret']})

@app.route("/api/create_credential_request", methods=["POST"])
def api_create_credential_request():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})

    # #testonly
    # get_cred_def_request = run_async( ledger.build_get_cred_def_request("4qk3Ab43ufPQVif4GAzLUW", "CHdq3VsmYm4iLsfhLturw4:3:CL:25:TAG3"))
    # get_cred_def_response = run_async(ledger.submit_request(user['pool'], get_cred_def_request))
    # cred_def_get = run_async( ledger.parse_get_cred_def_response(get_cred_def_response))

    # print(cred_def_get)
    if (user['master_secret'] == None):
        # read the file into user['master_secret']
        with open(f"../saves/user/{user['walletname']}/master_secret.json", "r") as master_secret_file:
            lines = master_secret_file.readlines()
            user['master_secret'] = lines[-1].strip()
    data = request.get_json()
    cred_offer = json.dumps(data.get("cred_offer"))
    
    cred_def = json.dumps(data.get("cred_def"))
    mydid = data.get("mydid")
    master_secret_id = user['master_secret']

    # print("asdasfawqfqw")

    if not cred_offer or not cred_def or not master_secret_id:
        return jsonify({"status": "error", "message": "Missing required fields"})
    cred_req, cred_req_metadata = run_async(anoncreds.prover_create_credential_req(user['wallet'], mydid, cred_offer, cred_def, master_secret_id))

    # please save cred req json into database
    # Ensure the directory exists
    directory = f"../saves/user/{user['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/cred_req.json", "a") as cred_req_file:
        cred_req_file.write(cred_req + "\n")

    # please save cred req metadate json into database
    # Ensure the directory exists
    directory = f"../saves/user/{user['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save schema json into database
    with open(f"{directory}/cred_req_metadata.json", "a") as cred_req_metadata_file:
        cred_req_metadata_file.write(cred_req_metadata + "\n")
    # print(cred_req)

    return jsonify({"status": "success", "message": cred_req, "metadata": cred_req_metadata})

@app.route("/api/list_cred_req", methods=["POST"])
def api_list_cred_req():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    with open(f"../saves/user/{user['walletname']}/cred_req.json", "r") as cred_req_file:
        cred_reqs = cred_req_file.readlines()
    cred_reqs = [cred_req.strip() for cred_req in cred_reqs]
    return jsonify({"status": "success", "message": cred_reqs})

@app.route("/api/list_cred_req_metadata", methods=["POST"])
def api_list_cred_req_metadata():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    with open(f"../saves/user/{user['walletname']}/cred_req_metadata.json", "r") as cred_req_metadata_file:
        cred_req_metadatas = cred_req_metadata_file.readlines()
    cred_req_metadatas = [cred_req_metadata.strip() for cred_req_metadata in cred_req_metadatas]
    return jsonify({"status": "success", "message": cred_req_metadatas})

@app.route("/api/store_credential", methods=["POST"])
def api_store_credential():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    cred = json.dumps(data.get("cred"))
    cred_req = json.dumps(data.get("cred_req"))
    cred_req_metadata = json.dumps(data.get("cred_req_metadata"))
    cred_def = json.dumps(data.get("cred_def"))
    if not cred or not cred_req or not cred_req_metadata or not cred_def:
        return jsonify({"status": "error", "message": "Missing required fields"})
    
    run_async(anoncreds.prover_store_credential(user['wallet'], None,   cred_req_metadata, cred, cred_def, None))
    

    return jsonify({"status": "success", "message": None})


@app.route("/api/get_credentials_for_proof_req", methods=["POST"])
def api_get_credentials_for_proof_req():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    # proof_req = json.dumps(data.get("proof_req"))
    # if not proof_req:
        # return jsonify({"status": "error", "message": "Missing required fields"})
    filter="{}"
    # print("proof_req", proof_req)
    res = run_async(anoncreds.prover_get_credentials(user['wallet'], filter))
    print("res", res)
    return jsonify({"status": "success", "message": res})

def preprocess_input(data, key):
    
    value = data.get(key, "")
    try:
        return json.loads(value)  # 如能解析为 JSON
    except:
        return value  # 否则直接返回字符串


@app.route("/api/create_proof", methods=["POST"])
def api_create_proof():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()

    # 获取数据（这些已经是字典了）
    proof_req_dict = data.get("proof_req", {})
    readyforproof_dict = data.get("readyforproof", {}) 
    schema_dict = data.get("schema", {})
    cred_def_dict = data.get("cred_def", {})

    # 确保它们是字符串格式
    proof_req_json = json.dumps(proof_req_dict)
    readyforproof_json = json.dumps(readyforproof_dict)
    schema_json = json.dumps(schema_dict)
    cred_def_json = json.dumps(cred_def_dict)

    # proof_req_json = json.dumps({ "nonce": "1432422343242122312411212", "name": "CitiBank-KYC", "version": "0.1", "requested_attributes": { "attr1_referent": { "name": "name", "restrictions": {"issuer_did": "STdrURQUU64d3JDUNbrc2T"} }, "attr2_referent": { "name": "age", "restrictions": {"issuer_did": "STdrURQUU64d3JDUNbrc2T"} }, "attr3_referent": { "name": "credit", "restrictions": {"issuer_did": "STdrURQUU64d3JDUNbrc2T"} }, "attr4_referent": { "name": "phonenumber" } }, "requested_predicates": { "predicate1_referent": { "name": "balance", "p_type": ">=", "p_value": 100000, "restrictions": {"issuer_did": "STdrURQUU64d3JDUNbrc2T"} } } })
    # readyforproof_json = json.dumps({ "self_attested_attributes": { "attr4_referent": "18001407169" }, "requested_attributes": { "attr1_referent": {"cred_id": "c83c7cf8-029d-4a60-b87a-43ac0871e055", "revealed": True}, "attr2_referent": {"cred_id": "c83c7cf8-029d-4a60-b87a-43ac0871e055", "revealed": True}, "attr3_referent": {"cred_id": "c83c7cf8-029d-4a60-b87a-43ac0871e055", "revealed": True} }, "requested_predicates": { "predicate1_referent": {"cred_id": "c83c7cf8-029d-4a60-b87a-43ac0871e055"} } }   )
    # schema_json= json.dumps({"STdrURQUU64d3JDUNbrc2T:2:PersonalAssets:1.0":{"ver": "1.0", "id": "STdrURQUU64d3JDUNbrc2T:2:PersonalAssets:1.0", "name": "PersonalAssets", "version": "1.0", "attrNames": ["balance", "credit", "age", "name"], "seqNo": 29}})
    # cred_def_json= json.dumps({"STdrURQUU64d3JDUNbrc2T:3:CL:29:tag1":{"ver":"1.0","id":"STdrURQUU64d3JDUNbrc2T:3:CL:29:tag1","schemaId":"29","type":"CL","tag":"tag1","value":{"primary":{"n":"96466546060672791872913619968688039606527644117424739513823502457301152837647823532693044155996461166672464036045010116048270198898028927548379590418008679048033183256350321074146556790190074644161185821609405323779026234100873772448127773639044199029189031617214406211981369965153366901336610476455202964078735607816905968670316184676941588684966399494164868019716122470472536064657553720197995996318561622758798321382269211813271675515036740993744918168078762598422308966732013493399167035145039561519277638143605419478450488682986529199317715930746809313964809606525848454241513452241380862378600929858499673404981","s":"19115172590839209002776821716187358417450130066562170756576532606060620458379072039048790122254586496855978914130698835111190004264323893331573986395554730031695311310417137142793581203526373788891360720680975435235945817561704725765721769440481589918025476634012611657670123498428464288408590862762515584618321770324883534624611724525711927119258037527714503856071537789676481098881467821764745124941908560804107887177173452023371428819839816499128769158558253072253993556872549685803758179605684965952797599506728184764297436242060838667618758366052481606810924678456614976985494258063189740584005506018207152334090","r":{"age":"13115438295120266430339376064594218955203582688034055566484652782511233203090263473991737293935634909008612786638632229572367612138811557271315559646596314460837341048538151791288655875949300190579657533817665538599840606324416200186893744346534733641484895326180156428317495344598418097594354650048065137541198612530990779811435453118754550825152084090669720607351019570583703013989863786621324399616241348642526802405619256293078950023197631785170706560541355111966335221083438632420802364951583932084729907052070593452610327421594712020409186274470770334784374380363450744957346695613285540592558101547399042400975","master_secret":"47247393763416380808069865903441994108803039608298055286514122378419567494867238294500613085562365980095577225579154570935098006885027259770294347696381237121218383406871479441727053835183431849435953780088954743166174852760581987132094140466679231065019018053222349883508529623444165714880783961121300779456468658851937028191302784398197475606392640702647588614292837005641133749500890577376494038434936855345944554157904515532911132137922388542698002998138365024104879240180709387544874375291947183686247768500953184122821800311612993796502173202998189795261194146802473577665697837226790752152695991902575043374332","name":"2174313032082966114375695788318150752315330835637835812365778337765054312371873162836061726545322956168322139738808243322916814833441530931323500323617025855698570522359939365742511788582213112038671083245057828882568380502662624981116661465719038996728635990503985357681793373513769116994099108855017984493615560603277667123299845617593951589337334893895951531139073713554354121254325089825425947092906592518114106639806350245689950134825647330814791193841735018154024601327266812768718699832029300612614758424719690295298337469823778066140557495160071319485862654533877485199985317624512046189247827338837980446741","balance":"45297684305745191404071336827481084111425074723208290860111739823621915511274053200773825661880813913499327870353302829016861108474901607461126867845647761590732611477841685971918503078813180456908125106098982454014360620517790936942420877200987497856131810961998464442091965511852597364206466136690615835286421126565725065981016549251478246029451303543058178886651575481337500239186034534470119831659304730224098585270128822442461778845163798619457320456125027324479931374248121568486816843608327058504923003870110696922593784644770428120552834697899187518370053945337860612472458415948380687371192174476019457785849","credit":"9070353847384652384138043562480256567097166598757171666094570536861057444584718157501545491105841662576738757048068041050791319706885511118376015869895011852918364525942948231876407443049405895174244393622299431854030798247026367245628471853945226982979215332318460277655717507136867667212061635998571180688649992636243882339255208208881410459075980653356987920744297800800269717512140798806396827555372646144006084596894807505570104017522936719944486574916919446830881923174266626653985874865240929135738312268367276981679599170082262835804225375907974657575600483489718408537611624114030743002692271677734328785412"},"rctxt":"11311285329480256654052835809378359742562357851406935225670582156362465558624223308256316472864851370674986944492865241623082224134978277642952721467275517117506156874966681105106327195440612094515611363169638774018129009924209965590533815833059532060911054351667763937906513368526723837529939423942802082309553717689580479827479562360574189952765806021813793021148286565414005085516426994377807064072561312758909192352007710219740203605753514366384229815263738763458859247613064011518269822519469205048561721364916357986259259073302313804001413076204406258605553299364529901955405683019857756101312714754623964284310","z":"62500251911774946393760081155323104783654597186301387885064528125356502236082113574819057077434196026480175134554640046391163452233407068787664223147585455990738151551035668394438846038226152856437855493133011508644688009123478736610934678111697283047176473325316046650468569968209846393112077560166573700382806124833067601026700131447845105351125470833051745085730477946498404450518441403170506281569983560855902117872736219218949061068504820066366012824224023004500064443638525388369355044097030276005769553144336586697019561071230500116171950586513563414267956243116333968456866255345912004886022243812182583689391"}}}})


    # 打印验证一下接收到的数据
    print("Received proof_req_json:", proof_req_json)
    print("Received readyforproof_json:", readyforproof_json)
    print("Received schema_json:", schema_json)
    print("Received cred_def_json:", cred_def_json)

    # get master_secret_id from file
    with open(f"../saves/user/{user['walletname']}/master_secret.json", "r") as master_secret_file:
        lines = master_secret_file.readlines()
        master_secret_id = lines[-1].strip()

    if not proof_req_json or not master_secret_id:
        return jsonify({"status": "error", "message": "Missing required fields"})
    
    res = run_async(anoncreds.prover_create_proof(user['wallet'], proof_req_json, readyforproof_json, master_secret_id, schema_json, cred_def_json, "{}"))

    # Save proof json into database
    directory = f"../saves/user/{user['walletname']}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/proof.json", "a") as proof_file:
        proof_file.write(res + "\n")

    return jsonify({"status": "success", "message": res})


@app.route("/api/list_proof", methods=["POST"])
def api_list_proof():
    if (user['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    with open(f"../saves/user/{user['walletname']}/proof.json", "r") as proof_file:
        proofs = proof_file.readlines()
    proofs = [proof.strip() for proof in proofs]
    return jsonify({"status": "success", "message": proofs})

if __name__ == "__main__":
    print("Initializing pool...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_pool())
    loop.close()
    app.run(host="0.0.0.0", port=5003, debug=1)
