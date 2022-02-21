from lib2to3.pgen2.literals import simple_escapes
from brownie import SimpleStorage, accounts

# If you want to just test one function, use "brownie test -k testing-funtion-name"
# "brownie test --pdb" will return you an testing error if test failed


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected


def test_updating_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    expected = 15
    simple_storage.store(expected, {"from": account})
    assert expected == simple_storage.retrieve()
