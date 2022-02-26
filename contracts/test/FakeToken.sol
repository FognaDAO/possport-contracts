pragma solidity ^0.8.0;

// THIS CONTRACT IS FOR TESTING PURPOSES AND IS NOT PART OF THE PROJECT

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract FakeToken is ERC1155, Ownable {

    constructor() ERC1155("https://game.example/api/item/{id}.json") {}

    function mint(address _to, uint256 _id, uint256 _amount) public onlyOwner {
        _mint(_to, _id, _amount, "");
    }

    function mintBatch(
        address _to,
        uint256[] calldata _ids,
        uint256[] calldata _amounts
    ) public onlyOwner {
        _mintBatch(_to, _ids, _amounts, "");
    }
}
