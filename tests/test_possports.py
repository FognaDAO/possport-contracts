from pytest import fixture
from brownie import accounts
from scripts import deploy

@fixture(scope="module", autouse=True)
def deployment():
    oldToken, token = deploy.local()
    yield oldToken, token

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

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
