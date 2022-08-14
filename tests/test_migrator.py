import brownie
from pytest import fixture
from brownie import accounts
from scripts import deploy, environment

BURN_ADDRESS = "0x000000000000000000000000000000000000dEaD"

env = environment.local

@fixture(scope="module", autouse=True)
def deployment():
    oldToken, token, migrator = deploy.local()
    yield oldToken, token, migrator

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_on_erc1155_received(deployment):
    oldToken, token, migrator = deployment
    token_id = 6
    old_token_id = env.tokens[token_id - 1].old_token_id
    assert oldToken.balanceOf(accounts[0], old_token_id) == 1
    old_balance = token.balanceOf(accounts[0])
    oldToken.safeTransferFrom(accounts[0], migrator, old_token_id, 1, "", {"from": accounts[0]})
    assert oldToken.balanceOf(accounts[0], old_token_id) == 0
    assert oldToken.balanceOf(migrator, old_token_id) == 0
    assert oldToken.balanceOf(BURN_ADDRESS, old_token_id) == 1
    assert token.balanceOf(accounts[0]) == old_balance + 1
    assert token.ownerOf(token_id) == accounts[0]

def test_on_erc1155_batch_received(deployment):
    oldToken, token, migrator = deployment
    old_token_ids = list(map(lambda t: t.old_token_id, env.tokens[:5]))
    oldToken.safeBatchTransferFrom(accounts[0], migrator, old_token_ids, [1] * len(old_token_ids), "", {"from": accounts[0]})
    for old_token_id in old_token_ids:
        assert oldToken.balanceOf(accounts[0], old_token_id) == 0
        assert oldToken.balanceOf(migrator, old_token_id) == 0
        assert oldToken.balanceOf(BURN_ADDRESS, old_token_id) == 1
    assert token.balanceOf(accounts[0]) == 5
    assert token.ownerOf(1) == accounts[0]

def test_on_erc1155_received_fail_with_different_token(deployment):
    oldToken, token, migrator = deployment
    id = 1
    other = deploy.fake_old_token([id])
    with brownie.reverts("invalid token contract"):
        other.safeTransferFrom(accounts[0], migrator, id, 1, "", {"from": accounts[0]})

def test_on_erc1155_batch_received_fail_with_different_token(deployment):
    oldToken, token, migrator = deployment
    ids = [1, 2, 3]
    other = deploy.fake_old_token(ids)
    with brownie.reverts("invalid token contract"):
        other.safeBatchTransferFrom(accounts[0], migrator, ids, [1, 1, 1], "", {"from": accounts[0]})
