import brownie
from pytest import fixture
from brownie import accounts
from scripts import deploy, environment

TOKENS = environment.polygon["tokens"]

@fixture(scope="module", autouse=True)
def token():
    token = deploy.poss_ports(accounts[0])
    for t in TOKENS:
        token._mint(accounts[0], t.newTokenId, t.tokenURI, {"from": accounts[0]})
    return token

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_set_default_royalty(token):
    tokenId = 1
    assert token.royaltyInfo(tokenId, 100) == (accounts[0], 10)
    token.adminSetDefaultRoyalty(accounts[1], 2000, {"from": accounts[0]})
    assert token.royaltyInfo(tokenId, 100) == (accounts[1], 20)

def test_burn(token):
    tokenId = 1
    assert token.ownerOf(tokenId) == accounts[0]
    old_balance = token.balanceOf(accounts[0])
    token.burn(tokenId, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == old_balance -1
    with brownie.reverts():
        token.ownerOf(tokenId)

def test_burn_fail_if_not_token_owner(token):
    tokenId = 1
    assert token.ownerOf(tokenId) != accounts[1]
    with brownie.reverts("caller is not owner nor approved"):
        token.burn(tokenId, {"from": accounts[1]})

def test_token_uri_updates(token):
    tokenId = 1
    token.adminSetBaseURI("", {"from": accounts[0]})
    token_uri = token.tokenURI(tokenId)
    token.adminSetBaseURI("http://", {"from": accounts[0]})
    assert token.tokenURI(tokenId) == "http://" + token_uri
    token.adminSetBaseEndURI("/end", {"from": accounts[0]})
    assert token.tokenURI(tokenId) == "http://" + token_uri + "/end"

def test_supports_interface(token):
    assert not token.supportsInterface("0x00000000")
    assert token.supportsInterface("0x80ac58cd") # ERC-721
    assert token.supportsInterface("0x5b5e139f") # ERC-721 Metadata
    assert token.supportsInterface("0x2a55205a") # ERC-721 Royalty

def test_transfer_from(token):
    tokenId = 1
    assert token.ownerOf(tokenId) == accounts[0]
    token.transferFrom(accounts[0], accounts[1], tokenId, {"from": accounts[0]})
    assert token.ownerOf(tokenId) == accounts[1]

def test_safe_transfer_from(token):
    tokenId = 2
    assert token.ownerOf(tokenId) == accounts[0]
    token.safeTransferFrom(accounts[0], accounts[1], tokenId, {"from": accounts[0]})
    assert token.ownerOf(tokenId) == accounts[1]    
