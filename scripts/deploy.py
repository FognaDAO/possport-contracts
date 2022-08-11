from brownie import PossPorts, UpgradeableProxy, TokenMigrator, FakeToken, Contract, web3, convert, accounts
from scripts import environment

DEFAULT_ROYALTY = 1000

def local():
    return _deploy(environment.local, accounts[0], accounts[0])

def polygon():
    return _deploy(environment.polygon, accounts[0], accounts[0])

def mumbai_testnet():
    return _deploy(environment.mumbai, accounts[0], accounts[0])

def _deploy(env, admin, upgrade_admin):
    old_token_ids = list(map(lambda t: t.old_token_id, env.tokens))
    token_uris = list(map(lambda t: t.uri, env.tokens))
    if (env.old_token):
        print("Using old ERC1155 token at %s", env.old_token)
        oldToken = FakeToken.at(env.old_token)
    else:
        print("No old token specified. Deploying a dummy ERC1155...")
        oldToken = fake_old_token(old_token_ids)
    token, migrator = token_with_migrator(
        oldToken,
        old_token_ids,
        token_uris,
        admin,
        env.opensea_proxy,
        upgrade_admin,
        env.publish_source
    )
    return oldToken, token, migrator

def token_with_migrator(
    old_token,
    old_token_ids,
    token_uris,
    admin,
    opensea_proxy,
    upgrade_admin,
    publish=False
):
    assert len(old_token_ids) == len(token_uris)
    migrator_address = accounts[0].get_deployment_address()
    token_address = accounts[0].get_deployment_address(accounts[0].nonce + 2)
    print("Deploying TokenMigrator contract...")
    migrator = TokenMigrator.deploy(
        old_token,
        token_address,
        old_token_ids,
        token_uris,
        {"from": accounts[0]},
        publish_source=publish
    )
    token = poss_ports(admin, migrator_address, opensea_proxy, upgrade_admin, publish)
    return token, migrator

def poss_ports(admin, minter, opensea_proxy, upgrade_admin, publish=False):
    # Deploy logic contract
    print("Deploying PossPorts contract...")
    logic = PossPorts.deploy({"from": accounts[0]}, publish_source=publish)
    # Deploy and initialize proxy contract
    initialize_call = logic.initialize.encode_input(admin, minter, opensea_proxy, DEFAULT_ROYALTY)
    print("Deploying UpgradeableProxy contract...")
    proxy = UpgradeableProxy.deploy(
        upgrade_admin,
        logic,
        initialize_call,
        {"from": accounts[0]},
        publish_source=publish
    )
    token = Contract.from_abi("PossPorts", proxy.address, PossPorts.abi + UpgradeableProxy.abi)
    return token

def fake_old_token(tokenIds):
    oldToken = FakeToken.deploy({"from": accounts[0]})
    oldToken.mintBatch(accounts[0], tokenIds, [1] * len(tokenIds))
    assert oldToken.balanceOf(accounts[0], tokenIds[0]) == 1
    return oldToken
