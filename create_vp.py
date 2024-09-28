import requests
import os
from dotenv import load_dotenv

load_dotenv()

tatum_api_key = os.getenv("TATUM_API_KEY")
private_key = os.getenv("PRIVATE_KEY")

url = "https://api.tatum.io/v3/polygon/smartcontract"

payload = {
    "contractAddress": "0x68708ffAE75696cff8264787776da758AAD2d0D9",
    "methodName": "createVP",
    "methodABI": {
        "constant": "false",
        "inputs": [
            { "name": "vpId", "type": "string" },
            { "name": "did", "type": "string" },
            { "name": "metadata", "type": "string" }
        ],
        "name": "createVP",
        "outputs": [],
        "payable": "false",
        "stateMutability": "nonpayable",
        "type": "function"
    },
    "params": ["vp:mexico:sellama", "did:0xE835e17D3276c14554014d5F96eb90672d73b201:name5", "Gerardo es mayor de edad"],
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