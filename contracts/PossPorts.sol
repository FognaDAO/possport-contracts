// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721RoyaltyUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";

import "@openzeppelin/contracts/utils/Base64.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

import "./OwnableLight.sol";
import "./interfaces/IContractFactory.sol";
import "./interfaces/ISewerActivities.sol";

contract PossPorts is ERC721RoyaltyUpgradeable, AccessControlUpgradeable, PausableUpgradeable, OwnableLight {

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    bytes32 public constant SOCIAL_RECOVERY_ROLE = keccak256("SOCIAL_RECOVERY_ROLE");

    bytes32 public constant ROYALTY_MANAGER_ROLE = keccak256("ROYALTY_MANAGER_ROLE");

    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    struct TokenData {
        string name;
        string description;
        string imageURI;
    }

    IContractFactory public activitiesFactory;

    string private baseImageURI;

    mapping(uint256 => TokenData) private tokenData;

    constructor() {
        // Prevents logic contract from being initialized
        _disableInitializers();
    }

    /**
    * @dev This can only be called once.
    * Should be called in the proxy contract right after instantiation.
    */
    function initialize(
        address admin,
        address owner,
        IContractFactory _activitiesFactory
    ) external initializer {
        baseImageURI = "ipfs://";
        activitiesFactory = _activitiesFactory;
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(MINTER_ROLE, admin);
        _grantRole(SOCIAL_RECOVERY_ROLE, admin);
        _grantRole(PAUSER_ROLE, admin);
        _transferOwnership(owner);
    }

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721RoyaltyUpgradeable, AccessControlUpgradeable) returns (bool) {
        return ERC721RoyaltyUpgradeable.supportsInterface(interfaceId) ||
            AccessControlUpgradeable.supportsInterface(interfaceId);
    }

    /**
     * @dev Override isApprovedForAll to auto-approve addresses with social recovery role.
     */
    function isApprovedForAll(address owner, address operator) public view virtual override returns (bool) {
        if (hasRole(SOCIAL_RECOVERY_ROLE, _msgSender())) {
            return true;
        }
        return super.isApprovedForAll(owner, operator);
    }

    /**
     * @dev See {IERC721Metadata-tokenURI}.
     */
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        address owner = ownerOf(tokenId);
        require (owner != address(0), "invalid token ID");
        TokenData memory data = tokenData[tokenId];
        ISewerActivities activities = ISewerActivities(activitiesFactory.currentContract());
        Points memory points = activities.points(owner);
        bytes memory dataURI = abi.encodePacked(
            '{"name":"', data.name,
            '","description":"', data.description,
            '","image":"', data.imageURI,
            '","attributes":[{"display_type":"boost_number","trait_type":"Community Points","value":"', Strings.toString(points.community),
            '"},{"display_type":"boost_number","trait_type":"Marketing Points","value":"', Strings.toString(points.marketing),
            '"},{"display_type":"boost_number","trait_type":"Treasury Points","value":"', Strings.toString(points.treasury),
            '"},{"display_type":"boost_number","trait_type":"Programming Points","value":"', Strings.toString(points.programming),
            '"}]}'
        );
        return string(abi.encodePacked("data:application/json;base64,", Base64.encode(dataURI)));
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
    * @dev Burn tokens that sender owns or is approved for.
    */
    function burn(uint256 tokenId) external {
        require(_msgSender() == ownerOf(tokenId) || _msgSender() == getApproved(tokenId), "caller is not owner nor approved");
        _burn(tokenId);
    }

    /**
     * @dev Owner can change default royalty information for all tokens.
     */
    function setDefaultRoyalty(address receiver, uint96 feeNumerator) external onlyRole(ROYALTY_MANAGER_ROLE) {
        _setDefaultRoyalty(receiver, feeNumerator);
    }

    /**
     * @dev Owner can set the royalty information for a specific token.
     */
    function setTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator) external onlyRole(ROYALTY_MANAGER_ROLE) {
        _setTokenRoyalty(tokenId, receiver, feeNumerator);
    }

    /**
     * @dev Owner can reset royalty information for a token back to the global default.
     */
    function ownerResetTokenRoyalty(uint256 tokenId) external onlyRole(ROYALTY_MANAGER_ROLE) {
        _resetTokenRoyalty(tokenId);
    }

    /**
     * @dev Minters can change token data.
     */
    function setTokenData(uint256 tokenId, TokenData calldata data) external onlyRole(MINTER_ROLE) {
        _setTokenData(tokenId, data);
    }

    /**
     * @dev Batched version of {ownerSetTokenURI}.
     */
    function batchSetTokenData(uint256[] calldata tokenIds, TokenData[] calldata data) external onlyRole(MINTER_ROLE) {
        require(tokenIds.length == data.length);
        for (uint256 i = 0; i < tokenIds.length; ++i) {
            _setTokenData(tokenIds[i], data[i]);
        }
    }

    /**
     * @dev Owner can change base URI.
     */
    function setBaseImageURI(string calldata newBaseURI) external onlyRole(MINTER_ROLE) {
        baseImageURI = newBaseURI;
    }

    /**
     * @dev This method is called by the migrator contract. The `_tokenURI` param was used in
     * the prevoius version of this contract, now it is ignored.
     */
    function _mint(address to, uint256 tokenId, string calldata _tokenURI) external onlyRole(MINTER_ROLE) {
        _mint(to, tokenId);
    }

    /**
     * @dev This method is called by the migrator contract. The `_tokenURIs` param was used in
     * the prevoius version of this contract, now it is ignored.
     */
    function _mintBatch(address to, uint256[] calldata tokenIds, string[] calldata tokenURIs) external onlyRole(MINTER_ROLE) {
        for (uint256 i = 0; i < tokenIds.length; ++i) {
            _mint(to, tokenIds[i]);
        }
    }

    /**
     * @dev Update token data. Internal function without access restriction.
     */
    function _setTokenData(uint256 tokenId, TokenData calldata data) internal {
        if (bytes(data.name).length > 0) {
            tokenData[tokenId].name = data.name;
        }
        if (bytes(data.description).length > 0) {
            tokenData[tokenId].description = data.description;
        }
        if (bytes(data.imageURI).length > 0) {
            tokenData[tokenId].imageURI = data.imageURI;
        }
    }
}
