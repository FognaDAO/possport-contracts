// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract UpgradeableProxy is ERC1967Proxy {

    constructor(
        address admin,
        address logic,
        bytes memory data
    ) ERC1967Proxy(logic, data) {
        _changeAdmin(admin);
    }

    /**
     * @dev Returns the current implementation address.
     */
    function getImplementation() external view returns (address) {
        return _implementation();
    }

    /**
     * See {ERC1967Upgrade-_getAdmin}.
     */
    function getAdmin() external view returns (address) {
        return _getAdmin();
    }

    /**
     * See {ERC1967Upgrade-_upgradeToAndCall}.
     */
    function upgradeToAndCall(
        address newImplementation,
        bytes memory data,
        bool forceCall
    ) external {
        require(_getAdmin() == msg.sender, "caller is not admin");
        _upgradeToAndCall(newImplementation, data, forceCall);
    }

    /**
     * See {ERC1967Upgrade-_changeAdmin}.
     */
    function changeAdmin(address newAdmin) external {
        require(_getAdmin() == msg.sender, "caller is not admin");
        _changeAdmin(newAdmin);
    }
}
