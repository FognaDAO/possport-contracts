import brownie
from pytest import fixture
from brownie import accounts
from scripts import deploy, environment

TOKENS = environment.polygon["tokens"]

@fixture(scope="module", autouse=True)
def deployment():
    oldToken, proxy, token, migrator = deploy.local()
    oldToken.setApprovalForAll(migrator, True, {"from": accounts[0]})
    yield oldToken, token, migrator

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_migrate(deployment):
    oldToken, token, migrator = deployment
    tokenId = 6
    oldTokenId = TOKENS[tokenId - 1].oldTokenId
    assert oldToken.balanceOf(accounts[0], oldTokenId) == 1
    old_balance = token.balanceOf(accounts[0])
    migrator.migrate(oldTokenId, {"from": accounts[0]})
    assert oldToken.balanceOf(accounts[0], oldTokenId) == 0
    assert token.balanceOf(accounts[0]) == old_balance + 1
    assert token.ownerOf(tokenId) == accounts[0]

def test_migrate_batch(deployment):
    oldToken, token, migrator = deployment
    oldTokenIds = list(map(lambda t: t.oldTokenId, TOKENS[:5]))
    oldToken.setApprovalForAll(token, True, {"from": accounts[0]})
    migrator.migrateBatch(oldTokenIds, [1] * 5, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == 5
    assert token.ownerOf(1) == accounts[0]

def test_migrate_fail_if_not_token_owner(deployment):
    oldToken, token, migrator = deployment
    tokenId = 25
    oldTokenId = TOKENS[tokenId - 1].oldTokenId
    assert oldToken.balanceOf(accounts[1], oldTokenId) == 0
    with brownie.reverts("ERC1155: caller is not token owner nor approved"):
        migrator.migrate(oldTokenId, {"from": accounts[1]})
