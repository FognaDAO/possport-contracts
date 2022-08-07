from brownie import FakeToken, PossPorts, UpgradeableProxy, Contract, web3, convert, accounts
from scripts import environment

OPENSEA_PROXY = "0x58807baD0B376efc12F5AD86aAc70E78ed67deaE"

def local():
    # Mint fake old tokens
    oldToken = FakeToken.deploy({"from": accounts[0]})
    oldTokenIds = list(map(lambda t: t.oldTokenId, environment.polygon["tokens"]))
    oldToken.mintBatch(accounts[0], oldTokenIds, [1] * len(oldTokenIds))
    assert oldToken.balanceOf(accounts[0], oldTokenIds[0]) == 1

    # Deploy PossPorts collection
    tokenURIs = list(map(lambda t: t.tokenURI, environment.polygon["tokens"]))
    logic = PossPorts.deploy({"from": accounts[0]})
    encoded_function_call = logic.initialize.encode_input(accounts[0], oldToken, OPENSEA_PROXY, oldTokenIds, tokenURIs)
    proxy = UpgradeableProxy.deploy(accounts[0], logic, encoded_function_call, {"from": accounts[0]})
    token = Contract.from_abi("PossPorts", proxy.address, PossPorts.abi)
    assert token.balanceOf(accounts[0]) == 0
    return oldToken, proxy, token
