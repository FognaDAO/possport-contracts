import brownie
from pytest import fixture
from scripts import deploy, environment
from brownie import PossPortsUpgrade, Contract, accounts

TOKENS = environment.polygon["tokens"]

@fixture(scope="module", autouse=True)
def deployment():
    oldToken, proxy, token = deploy.local()
    # Migrate all tokens
    oldTokenIds = list(map(lambda t: t.oldTokenId, TOKENS))
    oldToken.setApprovalForAll(token, True, {"from": accounts[0]})
    token.migrateBatch(oldTokenIds, [1] * len(TOKENS), {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == len(TOKENS)
    # Deploy new logic contract for testing
    new_logic = PossPortsUpgrade.deploy({"from": accounts[0]})
    yield new_logic, proxy

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_upgrade(deployment):
    new_logic, proxy = deployment
    # Upgrade proxy to new logic and call initialize() in the same transaction
    (replaced, new_value) = 13, 26
    proxy.upgradeToAndCall(new_logic, new_logic.initialize.encode_input(replaced, new_value), False, {"from": accounts[0]})
    token = Contract.from_abi("PossPortsUpgrade", proxy.address, PossPortsUpgrade.abi)
    assert token.replaced() == replaced
    assert token.newValue() == new_value
    assert token.baseURI() == "ipfs://"
    assert not token.baseEndURI()
    assert token.tokenURI(1) == "QmPnKZpXa7ypDWp8XEfsnZbCzhS5JC98S48pjtGXdb6Jb3"
    assert token.openseaProxy() == "0x58807baD0B376efc12F5AD86aAc70E78ed67deaE"
    assert token.balanceOf(accounts[0]) == 50
    tokenId = 1
    assert token.ownerOf(tokenId) == accounts[0]
    token.safeTransferFrom(accounts[0], accounts[1], tokenId, {"from": accounts[0]})
    assert token.ownerOf(tokenId) == accounts[1]

def test_change_admin(deployment):
    new_logic, proxy = deployment
    assert proxy.getAdmin() != accounts[1]
    proxy.changeAdmin(accounts[1], {"from": accounts[0]})
    assert proxy.getAdmin() == accounts[1]
    new_logic = PossPortsUpgrade.deploy({"from": accounts[0]})
    # Fail upgrade if not admin
    with brownie.reverts("caller is not admin"):
        proxy.upgradeToAndCall(new_logic, new_logic.initialize.encode_input(1, 1), False, {"from": accounts[0]})
    # Upgrade successfully if admin
    proxy.upgradeToAndCall(new_logic, new_logic.initialize.encode_input(1, 1), False, {"from": accounts[1]})
