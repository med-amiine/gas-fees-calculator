import os
import requests
from dotenv import load_dotenv

load_dotenv()

rpc_url = os.getenv('RPC_URL')

headers = {
    "Content-Type": "application/json"
}

payloads = [
    {
        "jsonrpc": "2.0",
        "method": "eth_gasPrice",
        "params": [],
        "id": 1
    },
    {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 2
    }
]

responses = []
for payload in payloads:
    response = requests.post(rpc_url, json=payload, headers=headers)
    responses.append(response.json())

gas_price = int(responses[0]['result'], 16)  # Convert from hex
block_number = int(responses[1]['result'], 16)

print(f"Gas Price: {gas_price} wei")
print(f"Block Number: {block_number}")

# (EIP-1559 compatible)
payload_base_fee = {
    "jsonrpc": "2.0",
    "method": "eth_getBlockByNumber",
    "params": ["latest", False],
    "id": 3
}

response_base_fee = requests.post(rpc_url, json=payload_base_fee, headers=headers)
latest_block = response_base_fee.json()
base_fee_per_gas = int(latest_block['result']['baseFeePerGas'], 16)

print(f"Base Fee per Gas: {base_fee_per_gas} wei")
