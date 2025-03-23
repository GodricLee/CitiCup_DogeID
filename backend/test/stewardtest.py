import requests
import uuid

url = "http://localhost:5001"

# res = requests.get(url=url + "/api/list_wallet")
# print(res.json())

# res = requests.post(url=url + "/api/open_wallet", json={"wallet_name": "steward2", "passwd": "steward2"})
# print(res.json())

# res = requests.get(url=url + "/api/list_did")
# print(res.json())

# res = requests.post(url=url + "/api/create_wallet", json={
#     "wallet_name": "wallet1",
#     "wallet_key": "114514",
# })
# print(res.json())


res = requests.post(url=url + "/api/open_wallet", json={
    "wallet_name": "wallet1",
    "wallet_key": "114514",
})
print(res.json())

# res = requests.post(url=url + "/api/create_did", json={
#     "seed": "000000000000000000000000Steward1",
# })
# print(res.json())

# res = requests.post(url=url + "/api/create_did", json={
#     "seed": "0000000000000000000000000Anchor1",
# })
# print(res.json())

res = requests.get(url=url + "/api/list_did", json={
    
})
print(res.json())

# res = requests.post(url=url + "/api/create_user", json={
#     "mydid": "Th7MpTaRZVRYnPiabds81Y",
#     "newdid": "CHdq3VsmYm4iLsfhLturw4",
#     "newverkey": "79oJWrV67fBiHoffC87XpyxahVmJg3x6qJ1EWRVMRPjw",
#     "role": "TRUST_ANCHOR",
# })
# print(res.json())