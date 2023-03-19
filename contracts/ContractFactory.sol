pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/proxy/Clones.sol";

interface Stoppable {
    function stop() external;
}

contract ContractFactory is AccessControl {
    bytes32 public constant CREATOR_ROLE = keccak256("CREATOR_ROLE");

    bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");

    address public currentContract;

    address public logic;

    event NewActivities(address newActivitiesContract);
    event LogicUpdate(address newLogic);

    constructor(address admin, address logicContract, bytes memory initData) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(CREATOR_ROLE, admin);
        _grantRole(UPDATER_ROLE, admin);
        logic = logicContract;
        // Create first activities contract
        currentContract = Clones.clone(logicContract);
        Address.functionCall(currentContract, initData);
        emit NewActivities(currentContract);
    }

    function newActivities(bool stopPrevious, bytes memory initData) external onlyRole(CREATOR_ROLE) {
        if (stopPrevious) {
            // Stop current activities
            Stoppable(currentContract).stop();
        }
        // Deploy new activities contract
        currentContract = Clones.clone(logic);
        // Initialize the new activities contract
        Address.functionCall(currentContract, initData);
        emit NewActivities(currentContract);
    }

    function updateLogic(address newLogic) external onlyRole(UPDATER_ROLE) {
        logic = newLogic;
        emit LogicUpdate(newLogic);
    }
}
