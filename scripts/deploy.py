from brownie import FakeToken, SewerTicketing, accounts

def test():
    pulci = 0
    possums = [1, 2, 3, 4, 5]
    token = fake_token(pulci, possums)
    ticketing = sewer_ticketing(token, pulci, possums)
    pulciAmount = token.balanceOf(accounts[0], pulci)
    token.safeTransferFrom(accounts[0], ticketing, pulci, pulciAmount, "", {"from": accounts[0]})
    return token, ticketing

def sewer_ticketing(token, pulci, possums):
    return SewerTicketing.deploy(token, pulci, possums, {"from": accounts[0]})

def fake_token(pulci, possums):
    token = FakeToken.deploy({"from": accounts[0]})
    # Mint possums and 4 pulci for each possum
    ids = possums + [pulci]
    amounts = ([1] * len(possums)) + [len(possums) * 4]
    token.mintBatch(accounts[0], ids, amounts)
    return token
