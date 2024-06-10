from web3 import Web3
import json
from dotenv import load_dotenv
import os

load_dotenv()

rpc_url = os.getenv('RPC_URL')
gas_price_contract= os.getenv('GAS_PRICE_ORACLE')
web3 = Web3(Web3.HTTPProvider(rpc_url))

with open('gas_price_oracle_abi.json', 'r') as abi_file:
    gas_oracle_abi = json.load(abi_file)

gas_oracle_address = web3.to_checksum_address(gas_price_contract)

gas_oracle_contract = web3.eth.contract(address=gas_oracle_address, abi=gas_oracle_abi)

l1_base_fee = gas_oracle_contract.functions.l1BaseFee().call()

l1_gas_used = gas_oracle_contract.functions.getL1GasUsed(b'').call()

scalar = gas_oracle_contract.functions.scalar().call()

l1_fee_calculated = l1_gas_used * l1_base_fee * scalar / 1000000

l1_fee_direct = gas_oracle_contract.functions.getL1Fee(b'').call()

print(f"L1 Base Fee: {l1_base_fee}")
print(f"L1 Gas Used: {l1_gas_used}")
print(f"Scalar: {scalar}")
print(f"Calculated L1 Fee: {l1_fee_calculated}")
print(f"Direct L1 Fee: {l1_fee_direct}")
