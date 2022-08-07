// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/utils/ERC1155Holder.sol";

interface NewToken {
    function _mint(
        address to,
        uint256 tokenId,
        string memory _tokenURI
    ) external;
}

contract TokenMigrator is ERC1155Holder {

    struct Token {
        uint256 id;
        string tokenURI;
    }

    mapping(uint256 => Token) private oldTokenIdMap;

    IERC1155 public oldToken;
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
        for (uint128 i = 0; i < oldTokenIds.length; i++) {
            oldTokenIdMap[oldTokenIds[i]] = Token(i + 1, tokenURIs[i]);
        }
    }

    /**
    * @dev Burn an old ERC1155 Possum on the OpenSea shared contract to
    * mint a new ERC721 Possum.
    */
    function migrate(uint256 oldTokenId) external {
        oldToken.safeTransferFrom(msg.sender, address(this), oldTokenId, 1, "");
        Token memory token = oldTokenIdMap[oldTokenId];
        require (token.id != 0, "invalid token id");
        newToken._mint(msg.sender, token.id, token.tokenURI);
    }

    /**
    * @dev Gas optimized method to migrate multiple tokens at once.
    * `amounts` must always be an array of the same size of `oldTokenIds`, all filled with `1`.
    * If it has a different value this function will fail or not transfer all the tokens.
    * Client is required to pre-compute this value in order to save gas.
    */
    function migrateBatch(uint256[] calldata oldTokenIds, uint256[] calldata amounts) external {
        oldToken.safeBatchTransferFrom(msg.sender, address(this), oldTokenIds, amounts, "");
        for (uint128 i = 0; i < oldTokenIds.length; i++) {
            Token memory token = oldTokenIdMap[oldTokenIds[i]];
            require (token.id != 0, "invalid token id");
            newToken._mint(msg.sender, token.id, token.tokenURI);
        }
    }
}
