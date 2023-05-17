// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

// THIS CONTRACT IS FOR TESTING PURPOSES AND IS NOT PART OF THE PROJECT

import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721RoyaltyUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC1155/utils/ERC1155HolderUpgradeable.sol";

import "../old/meta-transactions/ContextMixin.sol";
import "../old/meta-transactions/NativeMetaTransaction.sol";

contract PossPortsUpgrade is
    ERC721URIStorageUpgradeable,
    ERC721RoyaltyUpgradeable,
    OwnableUpgradeable,
    ContextMixin,
    NativeMetaTransaction {

    string public baseURI;
    string public baseEndURI;

    address public openseaProxy;

    uint256 public replaced;

    uint256 public newValue;

    function initialize(uint256 _replaced, uint256 _newValue) external reinitializer(2) {
        replaced = _replaced;
        newValue = _newValue;
    }

    function tokenURI(uint256 tokenId) public view override(ERC721URIStorageUpgradeable, ERC721Upgradeable) returns (string memory) {
        return ERC721URIStorageUpgradeable.tokenURI(tokenId);
    }

    function _burn(uint256 tokenId) internal override(ERC721URIStorageUpgradeable, ERC721RoyaltyUpgradeable) {
        ERC721URIStorageUpgradeable._burn(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721RoyaltyUpgradeable, ERC721Upgradeable) returns (bool) {
        return ERC721Upgradeable.supportsInterface(interfaceId);
    }
}
