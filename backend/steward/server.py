from flask import Flask, jsonify, request
import atexit

from indy import pool, wallet, did, ledger, blob_storage
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
    if steward['pool'] is not None:
        run_async(pool.close_pool_ledger(steward['pool']))
    if steward['wallet'] is not None:
        print("Closing wallet...")
        print("Wallet handle: ", steward['wallet'])
        run_async(wallet.close_wallet(steward['wallet']))
    loop.close()

atexit.register(shutdown)

steward = {
      'name': "Steward",
      'wallet_config': None,
      'wallet_credentials': None,
    #   'wallet_config': json.dumps({'id': 'sovrin_steward_wallet'}),
    #   'wallet_credentials': json.dumps({'key': 'steward_wallet_key'}),
      'pool': None,
      'seed': '000000000000000000000000Steward1',
      'wallet': None,
  }

async def initialize_pool():
    # pool_config = json.dumps({"genesis_txn": "/root/citi/poolfile"})
    # await pool.create_pool_ledger_config("testpool", pool_config)
    pool_handle = await pool.open_pool_ledger("testpool", None)
    steward['pool'] = pool_handle
    return pool_handle

async def initialize_wallet(wallet_name:str, wallet_key:str):
    # Create wallet
    steward['wallet_config'] = json.dumps({'id': wallet_name})
    steward['wallet_credentials'] = json.dumps({'key': wallet_key})
    await wallet.create_wallet(steward['wallet_config'], steward['wallet_credentials'])
    # wallet.create_wallet(steward['wallet_config'], steward['wallet_credentials'])
    steward['wallet'] = await wallet.open_wallet(steward['wallet_config'], steward['wallet_credentials'])

async def create_did(wallet_handle, seed=None):
    if seed is None:
        (steward['did'], steward['verkey']) = await did.create_and_store_my_did(wallet_handle, json.dumps({"seed": steward['seed']}))
    else:
        (steward['did'], steward['verkey']) = await did.create_and_store_my_did(wallet_handle, json.dumps({"seed": seed}))
    return steward['did'], steward['verkey']
    

@app.route("/api/create_wallet", methods=["POST"])
def api_create_wallet():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    wallet_key = data.get("wallet_key")
    steward['walletname'] = wallet_name
    if not wallet_name or not wallet_key:
        return jsonify({"status": "error", "message": "Missing required fields"})
    res=run_async(initialize_wallet(wallet_name, wallet_key))
    return jsonify({"status": "success", "message": res})
    
@app.route("/api/open_wallet", methods=["POST"])
def api_open_wallet():
    if(steward['wallet'] != None):
        run_async(wallet.close_wallet(steward['wallet']))
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    wallet_key = data.get("wallet_key")
    if not wallet_name or not wallet_key:
        return jsonify({"status": "error", "message": "Missing required fields"})
    steward["wallet"] = run_async(wallet.open_wallet(json.dumps({'id': wallet_name}), json.dumps({'key': wallet_key})))
    # 检查 steward["wallet"] 是否为整数
    if isinstance(steward["wallet"], int):
        return jsonify({"status": "success", "message": steward["wallet"]})
    else:
        return jsonify({"status": "error", "message": "Invalid wallet handle"})

@app.route("/api/create_did", methods=["POST"])
def api_create_did():
    if(steward['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    data = request.get_json()
    seed = data.get("seed")
    if not seed:
        return jsonify({"status": "error", "message": "Missing required fields"})
    res = run_async(create_did(steward['wallet'], seed))
    return jsonify({"status": "success", "message": res})
    
@app.route("/api/list_did", methods=["GET"])
def api_list_did():
    if (steward['wallet'] == None):
        return jsonify({"status": "error", "message": "Wallet not opened"})
    res= run_async(did.list_my_dids_with_meta(steward['wallet']))
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
    res = run_async(ledger.sign_and_submit_request(steward['pool'], steward['wallet'], mydid, nym_request))
    return jsonify({"status": "success", "message": res})

if __name__ == "__main__":
    print("Initializing pool...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_pool())
    loop.close()
    app.run(host="0.0.0.0", port=5001, debug=1)
