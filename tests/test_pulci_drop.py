from pytest import fixture
from brownie import accounts
from scripts import deploy

PULCI = 0
POSSUMS = [1, 2, 3, 4, 5]

@fixture(scope="module", autouse=True)
def deployment():
    token, ticketing = deploy.test()
    yield token, ticketing

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_claim_pulci(deployment):
    token, ticketing = deployment
    pulci_amount = token.balanceOf(accounts[0], PULCI)
    ticketing.claimPulci(accounts[0], POSSUMS[0], {"from": accounts[0]})
    assert token.balanceOf(accounts[0], PULCI) == pulci_amount + 4
    
