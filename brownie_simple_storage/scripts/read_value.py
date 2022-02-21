from brownie import SimpleStorage, accounts, config

# brownie console
# can be used to interact with the contract, like a shell
def read_contract():
    simple_storage = SimpleStorage[-1]  # [-1] interact with the most recent contract
    # go take the index thats one less than the length
    # ABI
    # Address
    print(simple_storage.retrieve())


def main():
    read_contract()
