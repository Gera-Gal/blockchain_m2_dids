import requests
import os
from dotenv import load_dotenv

load_dotenv()

tatum_api_key = os.getenv("TATUM_API_KEY")
private_key = os.getenv("PRIVATE_KEY")
print(tatum_api_key, private_key)
url = "https://api.tatum.io/v3/polygon/smartcontract"

payload = {
  "contractAddress": "0xE13D6ED71e86135CbbC60A0cb8659b0EAa758488",
  "methodName": "getDID",
  "methodABI": {
    "constant": "true",
    "inputs": [
      { "name": "did", "type": "string" }
    ],
    "name": "getDID",
    "outputs": [
        { "name":"", "type":"string" },
        { "name":"", "type":"address" },
        { "name":"", "type":"string" }
    ],
    "payable": "false",
    "stateMutability": "view",
    "type": "function"
  },
  "params": ["did:0xE835e17D3276c14554014d5F96eb90672d73b201:name5"],
  "fromPrivateKey": private_key
}

headers = {
    "x-api-key": tatum_api_key,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    result = response.json()
    transaction_id = result.get("txId", "No transaction ID found")
    data = result.get("data", "No data found")
    print(f'Transacción exitosa: {transaction_id}: {data}')
else:
    print(f"Error en la solicitud: {response.status_code} - {response.text}")