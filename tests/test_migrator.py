import brownie
from pytest import fixture
from brownie import accounts
from scripts import deploy, environment

env = environment.local

@fixture(scope="module", autouse=True)
def deployment():
    oldToken, token, migrator = deploy.local()
    oldToken.setApprovalForAll(migrator, True, {"from": accounts[0]})
    yield oldToken, token, migrator

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_migrate(deployment):
    oldToken, token, migrator = deployment
    token_id = 6
    old_token_id = env.tokens[token_id - 1].old_token_id
    assert oldToken.balanceOf(accounts[0], old_token_id) == 1
    old_balance = token.balanceOf(accounts[0])
    migrator.migrate(old_token_id, {"from": accounts[0]})
    assert oldToken.balanceOf(accounts[0], old_token_id) == 0
    assert token.balanceOf(accounts[0]) == old_balance + 1
    assert token.ownerOf(token_id) == accounts[0]

def test_migrate_batch(deployment):
    oldToken, token, migrator = deployment
    old_token_ids = list(map(lambda t: t.old_token_id, env.tokens[:5]))
    oldToken.setApprovalForAll(token, True, {"from": accounts[0]})
    migrator.migrateBatch(old_token_ids, [1] * 5, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == 5
    assert token.ownerOf(1) == accounts[0]

def test_migrate_fail_if_not_token_owner(deployment):
    oldToken, token, migrator = deployment
    token_id = 25
    old_token_id = env.tokens[token_id - 1].old_token_id
    assert oldToken.balanceOf(accounts[1], old_token_id) == 0
    with brownie.reverts("ERC1155: caller is not token owner nor approved"):
        migrator.migrate(old_token_id, {"from": accounts[1]})
