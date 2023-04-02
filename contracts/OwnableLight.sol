pragma solidity ^0.8.0;

/**
 * @dev This is a lightweight implementation of the OpenZeppelin Ownable contract interface.
 * There is an internal function to transfer ownership of the contract, but no public ones.
 *
 * Originally based on code by OpenZeppelin: https://github.com/OpenZeppelin/openzeppelin-contracts
 */
abstract contract OwnableLight {

    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view virtual returns (address) {
        return _owner;
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Internal function without access restriction.
     */
    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}
