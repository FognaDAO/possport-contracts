import brownie
from pytest import fixture
from scripts import deploy, environment
from brownie import SewerActivitiesLogic, accounts, reverts, web3

@fixture(scope="module", autouse=True)
def token():
    factory = deploy.activities_factory(accounts[0])
    token = SewerActivitiesLogic.at(factory.currentContract())
    tokenData1 = ("name1", "description1", "http://my-image.com", (1, 2, 3, 4))
    tokenData2 = ("name2", "description2", "", (2, 3, 4, 5))
    tokenData3 = ("name3", "description3", "", (3, 4, 5, 6))
    token.createAndMint(accounts[0], tokenData1, {"from": accounts[0]})
    token.createAndMint(accounts[0], tokenData2, {"from": accounts[0]})
    token.createAndMint(accounts[1], tokenData3, {"from": accounts[0]})
    yield token

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_mint(token):
    tokenId = 1
    assert token.balanceOf(accounts[1], tokenId) == 0
    assert token.points(accounts[1]) == (3, 4, 5, 6)
    token.mint(tokenId, accounts[1], {"from": accounts[0]})
    assert token.balanceOf(accounts[1], tokenId) == 1
    assert token.points(accounts[1]) == (4, 6, 8, 10)

def test_mint_to_many(token):
    tokenId = 1
    assert token.balanceOfBatch([accounts[1], accounts[2]], [tokenId, tokenId]) == [0, 0]
    assert token.points(accounts[1]) == (3, 4, 5, 6)
    assert token.points(accounts[2]) == (0, 0, 0, 0)
    token.mintToMany(tokenId, [accounts[1], accounts[2]], {"from": accounts[0]})
    assert token.balanceOfBatch([accounts[1], accounts[2]], [tokenId, tokenId]) == [1, 1]
    assert token.points(accounts[1]) == (4, 6, 8, 10)
    assert token.points(accounts[2]) == (1, 2, 3, 4)

def test_create_and_mint(token):
    tokenId = 4
    tokenData = ("name3", "description3", "http://image-3.com", (3, 3, 3, 3))
    assert token.points(accounts[1]) == (3, 4, 5, 6)
    token.createAndMint(accounts[1], tokenData, {"from": accounts[0]})
    assert token.balanceOf(accounts[1], tokenId) == 1
    assert token.uri(tokenId) == "data:application/json;base64,eyJuYW1lIjoibmFtZTMiLCJkZXNjcmlwdGlvbiI6ImRlc2NyaXB0aW9uMyIsImltYWdlIjoiaHR0cDovL2ltYWdlLTMuY29tImF0dHJpYnV0ZXMiOlt7ImRpc3BsYXlfdHlwZSI6Im51bWJlciIsInRyYWl0X3R5cGUiOiJDb21tdW5pdHkgUG9pbnRzIiwidmFsdWUiOiIzIn0seyJkaXNwbGF5X3R5cGUiOiJudW1iZXIiLCJ0cmFpdF90eXBlIjoiTWFya2V0aW5nIFBvaW50cyIsInZhbHVlIjoiMyJ9LHsiZGlzcGxheV90eXBlIjoibnVtYmVyIiwidHJhaXRfdHlwZSI6IlRyZWFzdXJ5IFBvaW50cyIsInZhbHVlIjoiMyJ9LHsiZGlzcGxheV90eXBlIjoibnVtYmVyIiwidHJhaXRfdHlwZSI6IlByb2dyYW1taW5nIFBvaW50cyIsInZhbHVlIjoiMyJ9XX0="
    assert token.points(accounts[1]) == (6, 7, 8, 9)

def test_create_and_mint_to_many(token):
    tokenId = 4
    tokenData = ("name4", "description4", "http://image-4.com", (3, 3, 3, 3))
    assert token.points(accounts[1]) == (3, 4, 5, 6)
    assert token.points(accounts[2]) == (0, 0, 0, 0)
    token.createAndMintToMany([accounts[1], accounts[2]], tokenData, {"from": accounts[0]})
    assert token.balanceOfBatch([accounts[1], accounts[2]], [tokenId, tokenId]) == [1, 1]
    assert token.tokenData(tokenId) == tokenData
    assert token.points(accounts[1]) == (6, 7, 8, 9)
    assert token.points(accounts[2]) == (3, 3, 3, 3)

def test_transfer_from(token):
    tokenId = 1
    assert token.points(accounts[0]) == (3, 5, 7, 9)
    assert token.points(accounts[1]) == (3, 4, 5, 6)
    assert token.balanceOf(accounts[0], tokenId) == 1
    token.safeTransferFrom(accounts[0], accounts[1], tokenId, 1, bytes(), {"from": accounts[0]})
    assert token.balanceOf(accounts[0], tokenId) == 0
    assert token.balanceOf(accounts[1], tokenId) == 1
    assert token.points(accounts[0]) == (2, 3, 4, 5)
    assert token.points(accounts[1]) == (4, 6, 8, 10)

def test_batch_transfer_from(token):
    tokenIds = [1, 2]
    assert token.points(accounts[0]) == (3, 5, 7, 9)
    assert token.points(accounts[1]) == (3, 4, 5, 6)
    assert token.balanceOfBatch([accounts[0]] * len(tokenIds), tokenIds) == [1, 1]
    token.safeBatchTransferFrom(accounts[0], accounts[1], tokenIds, [1] * len(tokenIds), bytes(), {"from": accounts[0]})
    assert token.balanceOfBatch([accounts[0]] * len(tokenIds), tokenIds) == [0, 0]
    assert token.balanceOfBatch([accounts[1]] * len(tokenIds), tokenIds) == [1, 1]
    assert token.points(accounts[0]) == (0, 0, 0, 0)
    assert token.points(accounts[1]) == (6, 9, 12, 15)

def test_revoke_role(token):
    minter_role = web3.keccak(text="MINTER_ROLE")
    assert token.hasRole(minter_role, accounts[0])
    # Check that address with minter role is able to mint
    token.mint(1, accounts[1], {"from": accounts[0]})
    # Revoke minter role
    token.revokeRole(minter_role, accounts[0], {"from": accounts[0]})
    assert not token.hasRole(minter_role, accounts[0])
    # Check that now minting transaction reverts
    with reverts():
        token.mint(1, accounts[1], {"from": accounts[0]})

def test_grant_role(token):
    minter_role = web3.keccak(text="MINTER_ROLE")
    assert not token.hasRole(minter_role, accounts[1])
    token.grantRole(minter_role, accounts[1], {"from": accounts[0]})
    assert token.hasRole(minter_role, accounts[1])
    token.mint(1, accounts[2], {"from": accounts[1]})


def test_supports_interface(token):
    assert not token.supportsInterface("0x0000dEaD")
    assert token.supportsInterface("0x01ffc9a7") # ERC165
    assert token.supportsInterface("0xd9b67a26") # ERC1155
    assert token.supportsInterface("0x0e89341c") # ERC1155MetadataURI
