from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
)

from brownie_fund_me.scripts.helpful_scripts import deploy_mocks

LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
FORKED_BLOCKCHAIN_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")

    if index:
        return accounts[index]

    # if we're doing local blockchain
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENT
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


"""This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
    Args:
        contract_name (string)
    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed
        version of this contract.
"""
contract_to_mock = {
    "eth_usd_price_fee": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        if len(contract_type) <= 0:
            # MockV3Aggregator length
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    mock_price_feed = MockV3Aggregator.deploy()

    print(f"The active network is {network.show_active()}")
    print(f"Deploying mocks...")

    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print("Mocks deployed!")
