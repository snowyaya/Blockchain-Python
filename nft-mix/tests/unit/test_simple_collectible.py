from lib2to3.pgen2.literals import simple_escapes
from scripts.helper_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
import pytest
from scripts.deploy_and_create import deploy_and_create


def test_can_create_simple_sollectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
