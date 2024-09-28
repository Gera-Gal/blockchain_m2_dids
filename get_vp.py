import requests
import os
from dotenv import load_dotenv

load_dotenv()

tatum_api_key = os.getenv("TATUM_API_KEY")
private_key = os.getenv("PRIVATE_KEY")

url = "https://api.tatum.io/v3/polygon/smartcontract"

payload = {
    "contractAddress": "0x68708ffAE75696cff8264787776da758AAD2d0D9",
    "methodName": "getVP",
    "methodABI": {
        "constant": "true",
        "inputs": [
            { "name": "vpId", "type": "string" }
        ],
        "name": "getVP",
        "outputs": [
            { "name": "", "type": "string" },
            { "name": "", "type": "string" },
            { "name": "", "type": "address" },
            { "name": "", "type": "string" },
            { "name": "", "type": "bool" }
        ],
        "payable": "false",
        "stateMutability": "view",
        "type": "function"
    },
    "params": ["vp:mexico:sellama"],
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