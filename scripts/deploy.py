from brownie import FakeToken, PossPorts, accounts

def local():
    oldToken = FakeToken.deploy({"from": accounts[0]})
    token = PossPorts.deploy(oldToken, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == 0
    # Mint 5 tokens, just for fun.
    token.mintBatch(accounts[0], [1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"])
    assert token.balanceOf(accounts[0]) == 5
    return oldToken, token

