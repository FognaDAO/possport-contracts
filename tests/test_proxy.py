import brownie
from pytest import fixture
from scripts import deploy, environment
from brownie import PossPortsUpgrade, Contract, accounts

env = environment.local

@fixture(scope="module", autouse=True)
def deployment():
    token = deploy.poss_ports(accounts[0], accounts[0], env.opensea_proxy, accounts[0])
    for t in env.tokens:
        token._mint(accounts[0], t.new_token_id, t.uri, {"from": accounts[0]})
    # Deploy new logic contract for testing
    new_logic = PossPortsUpgrade.deploy({"from": accounts[0]})
    yield new_logic, token

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_upgrade(deployment):
    new_logic, token = deployment
    # Upgrade proxy to new logic and call initialize() in the same transaction
    (replaced, new_value) = 13, 26
    token.upgradeToAndCall(new_logic, new_logic.initialize.encode_input(replaced, new_value), False, {"from": accounts[0]})
    token = Contract.from_abi("PossPortsUpgrade", token.address, PossPortsUpgrade.abi)
    assert token.replaced() == replaced
    assert token.newValue() == new_value
    assert token.baseURI() == "ipfs://"
    assert not token.baseEndURI()
    assert token.tokenURI(1) == "bafkreiadflw5nc747gf2vxn6sw5kkit5mef7sn4agx6pdhfmn7c6ahlfmy"
    assert token.openseaProxy() == "0x58807baD0B376efc12F5AD86aAc70E78ed67deaE"
    assert token.balanceOf(accounts[0]) == 50
    tokenId = 1
    assert token.ownerOf(tokenId) == accounts[0]
    token.safeTransferFrom(accounts[0], accounts[1], tokenId, {"from": accounts[0]})
    assert token.ownerOf(tokenId) == accounts[1]

def test_change_admin(deployment):
    new_logic, token = deployment
    assert token.getAdmin() != accounts[1]
    token.changeAdmin(accounts[1], {"from": accounts[0]})
    assert token.getAdmin() == accounts[1]
    new_logic = PossPortsUpgrade.deploy({"from": accounts[0]})
    # Fail upgrade if not admin
    with brownie.reverts("caller is not admin"):
        token.upgradeToAndCall(new_logic, new_logic.initialize.encode_input(1, 1), False, {"from": accounts[0]})
    # Upgrade successfully if admin
    token.upgradeToAndCall(new_logic, new_logic.initialize.encode_input(1, 1), False, {"from": accounts[1]})
