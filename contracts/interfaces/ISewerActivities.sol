// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

struct Points {
    uint32 community;
    uint32 marketing;
    uint32 treasury;
    uint32 programming;
}

interface ISewerActivities {

    function points(address account) external view returns (Points memory);
}
