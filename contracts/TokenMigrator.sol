// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/utils/ERC1155Receiver.sol";

interface NewToken {
    function _mint(address to, uint256 tokenId, string calldata tokenURI) external;
    function _mintBatch(address to, uint256[] calldata tokenIds, string[] calldata tokenURIs) external;
}

contract TokenMigrator is ERC1155Receiver {

    struct Token {
        uint256 id;
        string tokenURI;
    }

    address constant BURN_ADDRESS = 0x000000000000000000000000000000000000dEaD;

    /**
    * @dev Map ids on the old token contract to tokens in the new contract
    */
    mapping(uint256 => Token) private oldTokenIdMap;

    /**
    * @dev OpenSea shared token contract
    */
    IERC1155 public oldToken;

    /**
    * @dev New token contract
    */
    NewToken public newToken;

    constructor(
        address _oldToken,
        address _newToken,
        uint256[] memory oldTokenIds,
        string[] memory tokenURIs
    ) {
        require(oldTokenIds.length == tokenURIs.length);
        oldToken = IERC1155(_oldToken);
        newToken = NewToken(_newToken);
        for (uint256 i = 0; i < oldTokenIds.length; i++) {
            oldTokenIdMap[oldTokenIds[i]] = Token(i + 1, tokenURIs[i]);
        }
    }

    /**
    * @dev Burn received old ERC1155 Possum on the OpenSea shared contract to
    * mint a new ERC721 Possum.
    */
    function onERC1155Received(
        address operator,
        address from,
        uint256 oldTokenId,
        uint256 value,
        bytes calldata data
    ) external override returns (bytes4) {
        require (msg.sender == address(oldToken), "invalid token contract");
        require (value == 1);
        Token memory token = oldTokenIdMap[oldTokenId];
        require (token.id != 0, "invalid token id");
        newToken._mint(operator, token.id, token.tokenURI);
        oldToken.safeTransferFrom(address(this), BURN_ADDRESS, oldTokenId, 1, "");
        return this.onERC1155Received.selector;
    }

    /**
    * @dev Burn received old ERC1155 Possums on the OpenSea shared contract to
    * mint new ERC721 Possums.
    */
    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata oldTokenIds,
        uint256[] calldata values,
        bytes calldata data
    ) external override returns (bytes4) {
        require (msg.sender == address(oldToken), "invalid token contract");
        uint256[] memory newTokenIds = new uint256[](oldTokenIds.length);
        string[] memory newTokenURIs = new string[](oldTokenIds.length);
        for (uint256 i = 0; i < oldTokenIds.length; ++i) {
            require (values[i] == 1);
            Token memory token = oldTokenIdMap[oldTokenIds[i]];
            require (token.id != 0, "invalid token id");
            newTokenIds[i] = token.id;
            newTokenURIs[i] = token.tokenURI;
        }
        newToken._mintBatch(operator, newTokenIds, newTokenURIs);
        oldToken.safeBatchTransferFrom(address(this), BURN_ADDRESS, oldTokenIds, values, "");
        return this.onERC1155BatchReceived.selector;
    }
}
