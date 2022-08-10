pragma solidity ^0.8.0;

// THIS CONTRACT IS FOR TESTING PURPOSES AND IS NOT PART OF THE PROJECT

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract FakeToken is ERC1155, Ownable {

    constructor() ERC1155("https://game.example/api/item/{id}.json") {}

    function burn(address from, uint256 id, uint256 quantity) external {
        require (balanceOf(_msgSender(), id) >= quantity);
        _burn(from, id, quantity);
    }

    function mint(address to, uint256 id, uint256 amount) public onlyOwner {
        _mint(to, id, amount, "");
    }

    function mintBatch(
        address to,
        uint256[] calldata ids,
        uint256[] calldata amounts
    ) public onlyOwner {
        _mintBatch(to, ids, amounts, "");
    }
}
