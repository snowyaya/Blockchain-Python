# 0.019
# 19000000000000000000

from web3 import Web3
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
    get_account,
    fund_with_link,
    get_contract,
)
import pytest

# Before testing, need to delete the internal miannet fork
# brownie networks delete mainnet-fork

# Add development mainnet-fork to do testing
# brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/qYwkS2QuHTw3VRPrkNvW5CJWLuck3Xd-
# accounts=10 mnemonic=brownie port=8545
# => A new network 'mainnet-fork' has been added

# brownie test --network mainnet-fork


def test_get_entrance_fee():
    # account = accounts[0]
    # lottery = Lottery.deploy(
    #     config["networks"][network.show_active()]["eth_usd_price_feed"],
    #     {"from": account},
    # )
    # assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")

    # We only want to test this on a local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 2,000 eth / usd
    # usdEntranceFee is 50
    # 2000/1 == 50/x == 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()

    # Act, Assert
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    # Act, Assert
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    # Act, Assert
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()  # should get all the lottery winners
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    # 777 % 3 = 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0  # we have transferred all the money
    assert account.balance() == starting_balance_of_account + balance_of_lottery
