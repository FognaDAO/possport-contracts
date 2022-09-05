# PossPorts ERC721 collection contract
Possums NFT smart contract, written in [Solidity](https://docs.soliditylang.org/).

## Overview
Migrate old ERC1155 Possums hosted in the OpenSea Shared Contract to a new ERC721 collection deployed on a custom independent contract.

The ERC1155 interface enables interoperability for semi-fungible tokens, but, for totally not fungible NFTs like Possums, the ERC721 interface is much more convenient and easily enables cool features like on-chain voting.

We don't want our Possums to be locked on a shared multi-collection smart contract owned and controlled by OpenSea, assigned a long pseudo-random id, not able to be listed on different marketplaces. This contract is designed to handle this collection only, making much easier to build cool features on top of it. This also makes it easier to be listed on different marketplaces.

Still this contract fully supports OpenSea gasless transactions on Polygon. Metatransactions enable OpenSea to transfer your Possum and pay gas for you only if provided with a digital signature signed with your private key and verified on-chain, so it's not a security issue.

Before listing on OpenSea you still need to allow the OpenSea smart contract to transfer your Possums, and this unfortunately requires a gas fee. **Allowance to OpenSea contract is enabled by default**, this might be considered a security issue, so accounts have the option to disable this feature for their wallet calling `setOpenseaBlacklisted(true)`. OpenSea default allowance can also be globally disabled by owner address.

The PossPorts ERC721 contract is an upgradeable proxy using the [EIP-1967 Transparent Proxy pattern](https://eips.ethereum.org/EIPS/eip-1967). The Possum migration logic is handled by an immutable, uncontrolled contract.

The PossPorts ERC721 contract has an owner address that is allowed to:
- Turn off/on default allowance to OpenSea contract.
- Update Possums royalty infos, in compliance with [EIP-2981](https://eips.ethereum.org/EIPS/eip-2981).
- Update Possums metadata uri.
- Transfer ownership of this contract to a different address.

The PossPorts ERC721 contract olso has an admin address (different from owner) allowed to:
- Upgrade this contract to a different implementation.
- Transfer admin role to a different address.


## Testing and Development
Clone the repo to get started.

```bash
git clone https://gitlab.com/sewer-nation/possums.git
cd possums
```

### Docker development environment
You can use [Docker](https://www.docker.com/) to test and interact with smart contracts in a local development environment without the burden of installing anything else.

```bash
# build development Docker image based on current source code
docker build -t possums .

# run tests with 'brownie test'
docker run possums test

# run interactive 'brownie console'
docker run -it possums
```

### Dependencies
If you don't like *Docker*, you can install development dependencies manually.

* [python3](https://www.python.org/downloads/release/python-368/) - tested with version 3.8.10
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version 1.18.1
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version 6.12.2

We describe how to install development dependencies on Ubuntu 20.04, the same steps might apply to other operating systems.

We use [pipx](https://github.com/pypa/pipx) to install *Brownie* into a virtual environment and make it available directly from the commandline. You can also install *Brownie* via *pip*, in this case it is recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html). For more information about installing *Brownie* read the official [documentation](https://eth-brownie.readthedocs.io/en/stable/install.html#installing-brownie).

We use [node.js](https://nodejs.org/en/) and [npm](https://www.npmjs.com/) to install *ganache-cli* globally. We recommend installing the latest LTS versions of *node* and *npm* from [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) as we find versions in Ubuntu and Debian repositories to have [this](https://askubuntu.com/questions/1161494/npm-version-is-not-compatible-with-node-js-version) problem frequently.

```bash
sudo apt install curl gcc python3 python3-dev python3-venv pipx
pipx ensurepath

#install nvm
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.profile

# install node and npm using nvm
nvm install --lts=Gallium

# install ganache-cli
npm install ganache-cli@6.12.2 --global

# install brownie
pipx install eth-brownie==1.18.1
```

### Interacting with contracts
We use *Brownie* to compile, test and deploy our smart contracts. Please read the official [documentation](https://eth-brownie.readthedocs.io/en/stable/).

Use `brownie console` to compile contracts, launch and attach to a local test environment and interact to a command prompt very similar to a python shell.

```bash
brownie console
```

You can use the `local` function in the `deploy` script to deploy the *PossPorts* and *TokenMigrator* contracts on your local environment along with a fake ERC1155 token mocking the OpenSea Shared Contract. Then you can interact with the deployed contracts directly from the *Brownie* console.

After running the local deployment script your account owns all the 50 old ERC1155 Possums with their original ids. These ids are extremely long, we know they suck, but they were (pseudo)randomly generated by OpenSea and we can not have control over it, that's one of the many reasons we are migrating!

```python
# Run script that deploys everything needed
# oldToken: fake ERC1155 contract with all the 50 old Possums preminted and owned by your account
# token: new PossPorts ERC721 contract
# migrator: contract to handle Possum migration to the new ERC721 contract
oldToken, token, migrator = run('deploy', 'local')

account = accounts[0]

POSSUM_1 = 10110860822564241239994147652924744222037427536707093556420917645282000240641
POSSUM_2 = 10110860822564241239994147652924744222037427536707093556420917646381511868417

# account owns old fake Possums
assert oldToken.balanceOf(account, POSSUM_1) == 1
assert oldToken.balanceOf(account, POSSUM_2) == 1

# To migrate a possum simply transfer it to the migrator address
oldToken.safeTransferFrom(account, migrator, POSSUM_1, 1, bytes(), {"from": account})

# Congratulations! Now you own token with id 1 on the new ERC721 contract
assert token.ownerOf(1) == account
# And your old Possum is burned
assert oldToken.balanceOf(account, POSSUM_1) == 0
```

### Running tests
Test scripts are stored in the `tests/` directory of this project.

Use `brownie test` to run the complete test suite.

```bash
brownie test
```
