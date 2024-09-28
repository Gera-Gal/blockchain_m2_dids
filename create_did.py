import requests
import os
from dotenv import load_dotenv

load_dotenv()

tatum_api_key = os.getenv("TATUM_API_KEY")
private_key = os.getenv("PRIVATE_KEY")

url = "https://api.tatum.io/v3/polygon/smartcontract"

payload = {
  "contractAddress": "0xE13D6ED71e86135CbbC60A0cb8659b0EAa758488",
  "methodName": "createDID",
  "methodABI": {
    "constant": "false",
    "inputs": [
      { "name": "did", "type": "string" },
      { "name": "metadata", "type": "string" }
    ],
    "name": "createDID",
    "outputs": [],
    "payable": "false",
    "stateMutability": "nonpayable",
    "type": "function"
  },
  "params": ["did:mexico:1", "Gerardo Galicia Vargas"],
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
    print(f'Transacción exitosa: {transaction_id}')
else:
    print(f"Error en la solicitud: {response.status_code} - {response.text}")