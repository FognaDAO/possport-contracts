from brownie import PossPorts, UpgradeableProxy, TokenMigrator, FakeToken, Contract, web3, convert, accounts
from scripts import environment

TOKENS = environment.polygon["tokens"]

OPENSEA_PROXY = "0x58807baD0B376efc12F5AD86aAc70E78ed67deaE"
DEFAULT_ROYALTY = 1000

def local():
    old_token_ids = list(map(lambda t: t.oldTokenId, TOKENS))
    token_uris = list(map(lambda t: t.tokenURI, TOKENS))
    oldToken = fake_old_token(old_token_ids)
    token, migrator = token_with_migrator(oldToken, old_token_ids, token_uris)
    return oldToken, token, migrator

def token_with_migrator(old_token, old_token_ids, token_uris):
    assert len(old_token_ids) == len(token_uris)
    migrator_address = accounts[0].get_deployment_address()
    token_address = accounts[0].get_deployment_address(accounts[0].nonce + 2)
    migrator = TokenMigrator.deploy(old_token, token_address, old_token_ids, token_uris, {"from": accounts[0]})
    token = poss_ports(migrator_address)
    return token, migrator

def poss_ports(minter):
    # Deploy logic contract
    logic = PossPorts.deploy({"from": accounts[0]})
    # Deploy and initialize proxy contract
    initialize_call = logic.initialize.encode_input(accounts[0], minter, OPENSEA_PROXY, DEFAULT_ROYALTY)
    proxy = UpgradeableProxy.deploy(accounts[0], logic, initialize_call, {"from": accounts[0]})
    token = Contract.from_abi("PossPorts", proxy.address, PossPorts.abi + UpgradeableProxy.abi)
    return token

def fake_old_token(tokenIds):
    oldToken = FakeToken.deploy({"from": accounts[0]})
    oldToken.mintBatch(accounts[0], tokenIds, [1] * len(tokenIds))
    assert oldToken.balanceOf(accounts[0], tokenIds[0]) == 1
    return oldToken
