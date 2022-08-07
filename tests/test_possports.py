import brownie
from pytest import fixture
from brownie import accounts
from scripts import deploy, environment

@fixture(scope="module", autouse=True)
def deployment():
    oldToken, proxy, token = deploy.local()
    # Migrate 5 tokens
    oldTokenIds = list(map(lambda t: t.oldTokenId, environment.polygon["tokens"][:5]))
    oldToken.setApprovalForAll(token, True, {"from": accounts[0]})
    token.migrateBatch(oldTokenIds, [1] * 5, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == 5
    yield oldToken, token

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_migrate(deployment):
    oldToken, token = deployment
    tokenId = 6
    oldTokenId = environment.polygon["tokens"][tokenId - 1].oldTokenId
    assert oldToken.balanceOf(accounts[0], oldTokenId) == 1
    old_balance = token.balanceOf(accounts[0])
    token.migrate(oldTokenId, {"from": accounts[0]})
    assert oldToken.balanceOf(accounts[0], oldTokenId) == 0
    assert token.balanceOf(accounts[0]) == old_balance + 1
    assert token.ownerOf(tokenId) == accounts[0]

def test_migrate_fail_if_not_token_owner(deployment):
    oldToken, token = deployment
    tokenId = 25
    oldTokenId = environment.polygon["tokens"][tokenId - 1].oldTokenId
    assert oldToken.balanceOf(accounts[1], oldTokenId) == 0
    with brownie.reverts("ERC1155: caller is not token owner nor approved"):
        token.migrate(oldTokenId, {"from": accounts[1]})

def test_burn(deployment):
    oldToken, token = deployment
    tokenId = 1
    assert token.ownerOf(tokenId) == accounts[0]
    old_balance = token.balanceOf(accounts[0])
    token.burn(tokenId, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == old_balance -1
    with brownie.reverts():
        token.ownerOf(tokenId)

def test_burn_fail_if_not_token_owner(deployment):
    oldToken, token = deployment
    tokenId = 1
    assert token.ownerOf(tokenId) != accounts[1]
    with brownie.reverts("caller is not owner nor approved"):
        token.burn(tokenId, {"from": accounts[1]})

def test_token_uri_updates(deployment):
    oldToken, token = deployment
    tokenId = 1
    token.adminSetBaseURI("", {"from": accounts[0]})
    token_uri = token.tokenURI(tokenId)
    token.adminSetBaseURI("http://", {"from": accounts[0]})
    assert token.tokenURI(tokenId) == "http://" + token_uri
    token.adminSetBaseEndURI("/end", {"from": accounts[0]})
    assert token.tokenURI(tokenId) == "http://" + token_uri + "/end"

def test_supports_interface(deployment):
    oldToken, token = deployment
    assert not token.supportsInterface("0x00000000")
    assert token.supportsInterface("0x80ac58cd") # ERC-721
    assert token.supportsInterface("0x5b5e139f") # ERC-721 Metadata
    assert token.supportsInterface("0x2a55205a") # ERC-721 Royalty

def test_transfer_from(deployment):
    oldToken, token = deployment
    tokenId = 1
    assert token.ownerOf(tokenId) == accounts[0]
    token.transferFrom(accounts[0], accounts[1], tokenId, {"from": accounts[0]})
    assert token.ownerOf(tokenId) == accounts[1]

def test_safe_transfer_from(deployment):
    oldToken, token = deployment
    tokenId = 2
    assert token.ownerOf(tokenId) == accounts[0]
    token.safeTransferFrom(accounts[0], accounts[1], tokenId, {"from": accounts[0]})
    assert token.ownerOf(tokenId) == accounts[1]    
