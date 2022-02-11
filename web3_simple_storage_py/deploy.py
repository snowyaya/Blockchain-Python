import json
from web3 import Web3
from solcx import compile_standard, install_solc

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# print("Installing...")
install_solc("0.6.0")

# Compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print(abi)

# for connecting to gagache
w3 = Web3(Web3.HTTPProvide("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0xF9F8E9623B3749D385EE7B82AE5D182DB381FE4B"
private_key = "0x93e828467ca2249b4a0c0fb0e684d0dd18db33b488235b3a9b47aed1c737454b"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
