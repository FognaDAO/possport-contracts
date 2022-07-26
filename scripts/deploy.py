from brownie import FakeToken, PossPorts, accounts
from scripts import environment

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

def local():
    # Mint fake old tokens
    oldToken = FakeToken.deploy({"from": accounts[0]})
    oldTokenIds = list(map(lambda t: t.oldTokenId, environment.polygon["tokens"]))
    oldToken.mintBatch(accounts[0], oldTokenIds, [1] * len(oldTokenIds))
    assert oldToken.balanceOf(accounts[0], oldTokenIds[0]) == 1

    # Deploy PossPorts collection
    tokenURIs = list(map(lambda t: t.tokenURI, environment.polygon["tokens"]))
    token = PossPorts.deploy(oldToken, ZERO_ADDRESS, oldTokenIds, tokenURIs, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == 0
    return oldToken, token
