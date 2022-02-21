# we can directly import the contract
from brownie import accounts, config, SimpleStorage, network

# import os


def deploy_simple_storage():
    account = get_account()
    # brownie allows us directly import and deploy the contract instead of doing many steps (abi, once..)
    simple_storage = SimpleStorage.deploy({"from": account})
    # print(simple_storage)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)

    # use command line to get an encrypted account
    # brownie account new account-name
    # account = accounts.load("blockchain-python-account")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))

    # works the same as os.getenv()
    # account = accounts.add(config["wallets"]["from_key"])


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
