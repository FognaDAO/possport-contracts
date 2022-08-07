// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";

import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721RoyaltyUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC1155/utils/ERC1155HolderUpgradeable.sol";

import "./meta-transactions/ContextMixin.sol";
import "./meta-transactions/NativeMetaTransaction.sol";

contract PossPorts is
    ERC721URIStorageUpgradeable,
    ERC721RoyaltyUpgradeable,
    OwnableUpgradeable,
    ERC1155HolderUpgradeable,
    ContextMixin,
    NativeMetaTransaction {

    struct Token {
        uint256 id;
        string tokenURI;
    }

    IERC1155 private oldContract;

    string private baseURI;
    string private baseEndURI;

    mapping(uint256 => Token) private oldTokenIdMap;

    /**
    * For Polygon mainnet use 0x58807baD0B376efc12F5AD86aAc70E78ed67deaE
    * For Mumbai testnet use 0xff7Ca10aF37178BdD056628eF42fD7F799fAc77c
    */
    address private openseaProxy;

    constructor() {
        // Prevents logic contract from being initialized
        _disableInitializers();
    }

    /**
    * This can only be called once.
    * Should be called in the proxy contract right after instantiation.
     */
    function initialize(
        address admin,
        address _oldContract,
        address _openseaProxy,
        uint96 royalty,
        uint256[] calldata oldTokenIds,
        string[] calldata tokenURIs
    ) external initializer {
        require(oldTokenIds.length == tokenURIs.length);
        __ERC721_init("PossPorts", "POSSUM");
        _initializeEIP712("PossPorts");
        _transferOwnership(admin);
        _setDefaultRoyalty(admin, royalty);
        baseURI = "ipfs://";
        openseaProxy = _openseaProxy;
        oldContract = IERC1155(_oldContract);
        for (uint128 i = 0; i < oldTokenIds.length; i++) {
            oldTokenIdMap[oldTokenIds[i]] = Token(i + 1, tokenURIs[i]);
        }
    }

    /**
    * @dev Burn an old ERC1155 Possum on the OpenSea shared contract to
    * mint a new ERC721 Possum.
    */
    function migrate(uint256 oldTokenId) external {
        oldContract.safeTransferFrom(_msgSender(), address(this), oldTokenId, 1, "");
        Token memory newToken = oldTokenIdMap[oldTokenId];
        require (newToken.id != 0, "invalid token id");
        _mint(_msgSender(), newToken.id, newToken.tokenURI);
    }

    /**
    * @dev Gas optimized method to migrate multiple tokens at once.
    * `amounts` must always be an array of the same size of `oldTokenIds`, all filled with `1`.
    * If it has a different value this function will fail or not transfer all the tokens.
    * Client is required to pre-compute this value in order to save gas.
    */
    function migrateBatch(uint256[] calldata oldTokenIds, uint256[] calldata amounts) external {
        oldContract.safeBatchTransferFrom(_msgSender(), address(this), oldTokenIds, amounts, "");
        for (uint128 i = 0; i < oldTokenIds.length; i++) {
            Token memory newToken = oldTokenIdMap[oldTokenIds[i]];
            require (newToken.id != 0, "invalid token id");
            _mint(_msgSender(), newToken.id, newToken.tokenURI);
        }
    }

    /**
    * @dev Burn tokens that sender owns or is approved for.
    */
    function burn(uint256 tokenId) external {
        require(_msgSender() == ownerOf(tokenId) || _msgSender() == getApproved(tokenId), "caller is not owner nor approved");
        _burn(tokenId);
    }

    /**
     * @dev Override isApprovedForAll to auto-approve OpenSea's proxy contract.
     */
    function isApprovedForAll(address owner, address operator) public view virtual override returns (bool) {
        // if OpenSea's ERC721 Proxy Address is detected, auto-return true
        if (operator == openseaProxy) {
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
    function supportsInterface(bytes4 interfaceId) public view override(ERC721RoyaltyUpgradeable, ERC1155ReceiverUpgradeable, ERC721Upgradeable) returns (bool) {
        return ERC721RoyaltyUpgradeable.supportsInterface(interfaceId)
        || ERC721Upgradeable.supportsInterface(interfaceId)
        || ERC1155ReceiverUpgradeable.supportsInterface(interfaceId);
    }

    /**
     * @dev Admin can change default royalty information for all tokens.
     */
    function adminSetDefaultRoyalty(address receiver, uint96 feeNumerator) external onlyOwner {
        _setDefaultRoyalty(receiver, feeNumerator);
    }

    /**
     * @dev Admin can set the royalty information for a specific token.
     */
    function adminSetTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator) external onlyOwner {
        _setTokenRoyalty(tokenId, receiver, feeNumerator);
    }

    /**
     * @dev Admin can remove default royalty information.
     */
    function adminDeleteDefaultRoyalty() external onlyOwner {
        _deleteDefaultRoyalty();
    }

    /**
     * @dev Admin can reset royalty information for a token back to the global default.
     */
    function adminResetTokenRoyalty(uint256 tokenId) external onlyOwner {
        _resetTokenRoyalty(tokenId);
    }

    /**
     * @dev Admin can change token URI.
     */
    function adminSetTokenURI(uint256 tokenId, string calldata _tokenURI) external onlyOwner {
        _setTokenURI(tokenId, _tokenURI);
    }

    /**
     * @dev Admin can change base URI.
     */
    function adminSetBaseURI(string calldata baseURI_) external onlyOwner {
        baseURI = baseURI_;
    }

    /**
     * @dev Admin can change base end URI.
     */
    function adminSetBaseEndURI(string calldata baseEndURI_) external onlyOwner {
        baseEndURI = baseEndURI_;
    }

    /**
     * @dev See {ERC721-_mint}.
     */
    function _mint(address to, uint256 tokenId, string memory _tokenURI) internal {
        _mint(to, tokenId);
        _setTokenURI(tokenId, _tokenURI);
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
