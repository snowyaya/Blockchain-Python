# 0.019
# 19000000000000000000

from web3 import Web3
from brownie import Lottery, accounts, config, network

# Before testing, need to delete the internal miannet fork
# brownie networks delete mainnet-fork

# Add development mainnet-fork to do testing
# brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/qYwkS2QuHTw3VRPrkNvW5CJWLuck3Xd-
# accounts=10 mnemonic=brownie port=8545
# => A new network 'mainnet-fork' has been added

# brownie test --network mainnet-fork


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    # assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")
