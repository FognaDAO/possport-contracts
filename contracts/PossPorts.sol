// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721RoyaltyUpgradeable.sol";

import "./meta-transactions/ContextMixin.sol";
import "./meta-transactions/NativeMetaTransaction.sol";

contract PossPorts is
    ERC721URIStorageUpgradeable,
    ERC721RoyaltyUpgradeable,
    OwnableUpgradeable,
    ContextMixin,
    NativeMetaTransaction {

    string private baseURI;
    string private baseEndURI;

    /**
    * @dev OpenSea's ERC721 Proxy Address.
    * For Polygon mainnet use 0x58807baD0B376efc12F5AD86aAc70E78ed67deaE
    * For Mumbai testnet use 0xff7Ca10aF37178BdD056628eF42fD7F799fAc77c
    */
    address public openseaProxy;

    /**
    * @dev If true, OpenSea's Proxy Address is approved by default for all tokens.
    */
    bool public openseaDefaultApproval;

    /**
    * @dev If OpenSea is blacklisted for some address, then OpenSea's Proxy Address
    * default approval does not apply for that address.
    */
    mapping (address => bool) public hasBlacklistedOpensea;

    /**
    * @dev The only address that can mint tokens. It is an immutable contract.
    */
    address public minter;

    constructor() {
        // Prevents logic contract from being initialized
        _disableInitializers();
    }

    /**
    * @dev This can only be called once.
    * Should be called in the proxy contract right after instantiation.
    */
    function initialize(
        address owner,
        address _minter,
        address _openseaProxy,
        uint96 royalty
    ) external initializer {
        __ERC721_init("PossPorts", "POSSUM");
        _initializeEIP712("PossPorts");
        _transferOwnership(owner);
        _setDefaultRoyalty(owner, royalty);
        openseaDefaultApproval = true;
        baseURI = "ipfs://";
        minter = _minter;
        openseaProxy = _openseaProxy;
    }

    /**
    * @dev Anyone can blacklist OpenSea's Proxy Address.
    */
    function setOpenseaBlacklisted(bool blacklisted) external {
        hasBlacklistedOpensea[_msgSender()] = blacklisted;
    }

    /**
    * @dev Burn tokens that sender owns or is approved for.
    */
    function burn(uint256 tokenId) external {
        require(_msgSender() == ownerOf(tokenId) || _msgSender() == getApproved(tokenId), "caller is not owner nor approved");
        _burn(tokenId);
    }

    /**
     * @dev Batched version of of {IERC721-ownerOf}.
     */
     function ownerOfBatch(uint256[] calldata tokenIds) external view returns (address[] memory) {
        address[] memory owners = new address[](tokenIds.length);
        for(uint256 i = 0; i < tokenIds.length; ++i) {
            owners[i] = ownerOf(tokenIds[i]);
        }
        return owners;
    }

    /**
     * @dev Override isApprovedForAll to auto-approve OpenSea's proxy contract.
     */
    function isApprovedForAll(address owner, address operator) public view virtual override returns (bool) {
        // OpenSea is allowed if default approval is enabled and owner has not blacklisted OpenSea
        if (operator == openseaProxy && openseaDefaultApproval && !hasBlacklistedOpensea[owner]) {
            return true;
        }
        return super.isApprovedForAll(owner, operator);
    }

    /**
     * @dev See {IERC721Metadata-tokenURI}.
     */
     function tokenURI(uint256 tokenId) public view override(ERC721URIStorageUpgradeable, ERC721Upgradeable) returns (string memory) {
        string memory uri = ERC721URIStorageUpgradeable.tokenURI(tokenId);
        return bytes(baseEndURI).length == 0 ? uri : string(abi.encodePacked(uri, baseEndURI));
    }

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view override(ERC721RoyaltyUpgradeable, ERC721Upgradeable) returns (bool) {
        return ERC721RoyaltyUpgradeable.supportsInterface(interfaceId) ||
            ERC721Upgradeable.supportsInterface(interfaceId);
    }

    /**
     * @dev Owner can change default royalty information for all tokens.
     */
    function ownerSetDefaultRoyalty(address receiver, uint96 feeNumerator) external onlyOwner {
        _setDefaultRoyalty(receiver, feeNumerator);
    }

    /**
     * @dev Owner can set the royalty information for a specific token.
     */
    function ownerSetTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator) external onlyOwner {
        _setTokenRoyalty(tokenId, receiver, feeNumerator);
    }

    /**
     * @dev Owner can remove default royalty information.
     */
    function ownerDeleteDefaultRoyalty() external onlyOwner {
        _deleteDefaultRoyalty();
    }

    /**
     * @dev Owner can reset royalty information for a token back to the global default.
     */
    function ownerResetTokenRoyalty(uint256 tokenId) external onlyOwner {
        _resetTokenRoyalty(tokenId);
    }

    /**
     * @dev Owner can change token URI.
     */
    function ownerSetTokenURI(uint256 tokenId, string calldata newTokenURI) external onlyOwner {
        _setTokenURI(tokenId, newTokenURI);
    }

    /**
     * @dev Batched version of {ownerSetTokenURI}.
     */
    function ownerBatchSetTokenURIs(uint256[] calldata tokenIds, string[] calldata newTokenURIs) external onlyOwner {
        require(tokenIds.length == newTokenURIs.length);
        for (uint256 i = 0; i < tokenIds.length; ++i) {
            _setTokenURI(tokenIds[i], newTokenURIs[i]);
        }
    }

    /**
     * @dev Owner can change base URI.
     */
    function ownerSetBaseURI(string calldata newBaseURI) external onlyOwner {
        baseURI = newBaseURI;
    }

    /**
     * @dev Owner can change base end URI.
     */
    function ownerSetBaseEndURI(string calldata newBaseEndURI) external onlyOwner {
        baseEndURI = newBaseEndURI;
    }

    /**
     * @dev Owner can enable or disable OpenSea's Proxy Address default approval.
     */
    function ownerSetOpenseaDefaultApproval(bool approved) external onlyOwner {
        openseaDefaultApproval = approved;
    }

    /**
     * @dev Only minter is able to mint new tokens.
     */
    function _mint(address to, uint256 tokenId, string calldata _tokenURI) external {
        require (_msgSender() == minter, "caller is not the minter");
        _mint(to, tokenId);
        _setTokenURI(tokenId, _tokenURI);
    }

    /**
     * @dev Minter can mint multiple tokens in one transaction.
     */
    function _mintBatch(address to, uint256[] calldata tokenIds, string[] calldata tokenURIs) external {
        require (_msgSender() == minter, "caller is not the minter");
        require(tokenIds.length == tokenURIs.length);
        for (uint256 i = 0; i < tokenIds.length; ++i) {
            _mint(to, tokenIds[i]);
            _setTokenURI(tokenIds[i], tokenURIs[i]);
        }
    }

    /**
     * @dev See {ERC721-_burn}.
     */
    function _burn(uint256 tokenId) internal override(ERC721URIStorageUpgradeable, ERC721RoyaltyUpgradeable) {
        ERC721URIStorageUpgradeable._burn(tokenId);
        _resetTokenRoyalty(tokenId);
    }

    /**
     * @dev This is used instead of msg.sender as transactions might be
     * sent by OpenSea instead of the original owner.
     */
    function _msgSender() internal view virtual override returns (address) {
        return ContextMixin.msgSender();
    }

    /**
     * @dev See {ERC721-_baseURI}. The resulting URI for each
     * token will be `baseURI + tokenId + baseEndURI`.
     */
    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }
}
