pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";

import "@openzeppelin/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

import "@openzeppelin/contracts/utils/Base64.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

import "./ERC1155Soulbound.sol";

contract SewerActivitiesLogic is
    ERC1155Soulbound,
    AccessControl,
    Initializable,
    IERC1155MetadataURI
{
    struct TokenData {
        string name;
        string description;
        string imageURI;
        uint32 communityPoints;
        uint32 marketingPoints;
        uint32 treasuryPoints;
        uint32 programmingPoints;
    }

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    bytes32 public constant TERMINATOR_ROLE = keccak256("TERMINATOR_ROLE");

    bytes32 public constant SOCIAL_RECOVERY_ROLE = keccak256("SOCIAL_RECOVERY_ROLE");

    mapping(uint256 => TokenData) public tokenData;

    /**
     * @dev When contract is stopped no more tokens can be minted
     */
    bool public stopped;

    uint256 private tokenIdCounter;

    // Used as the default URI for all token images
    string private defaultTokenImage;

    constructor() {
        // Prevents logic contract from being initialized
        _disableInitializers();
    }

    /**
     * @dev This can only be called once.
     * Should be called right after instantiation.
     */
    function initialize(
        address admin,
        address minter,
        address socialRecovery,
        string calldata tokenImage
    ) external initializer {
        stopped = false;
        defaultTokenImage = tokenImage;
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(MINTER_ROLE, minter);
        _grantRole(SOCIAL_RECOVERY_ROLE, socialRecovery);
        _grantRole(TERMINATOR_ROLE, _msgSender());
    }

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view override(ERC1155Soulbound, AccessControl, IERC165) returns (bool) {
        return
            ERC1155Soulbound.supportsInterface(interfaceId) ||
            interfaceId == type(IERC1155MetadataURI).interfaceId ||
            AccessControl.supportsInterface(interfaceId);
    }

    /**
     * @dev See {IERC1155MetadataURI-uri}.
     */
    function uri(uint256 id) external view override returns (string memory) {
        TokenData memory data = tokenData[id];
        bytes memory dataURI = abi.encodePacked(
            '{"name":"', data.name,
            '","description":"', data.description,
            '","image":"', bytes(data.imageURI).length > 0 ? data.imageURI : defaultTokenImage,
            '","properties":{"community_points":', Strings.toString(data.communityPoints),
            ',"marketing_points":', Strings.toString(data.marketingPoints),
            ',"treasury_points":', Strings.toString(data.treasuryPoints),
            ',"programming_points":', Strings.toString(data.programmingPoints),
            "}}"
        );
        return string(abi.encodePacked("data:application/json;base64,", Base64.encode(dataURI)));
    }

    /**
     * @dev Soulbound tokens can only be transfered for social recovery.
     * See {IERC1155-safeTransferFrom}.
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public override(ERC1155Soulbound, IERC1155) onlyRole(SOCIAL_RECOVERY_ROLE) {
        _safeTransferFrom(from, to, id, amount, data);
    }

    /**
     * @dev Soulbound tokens can only be transfered for social recovery..
     * See {IERC1155-safeBatchTransferFrom}.
     */
    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) public virtual override(ERC1155Soulbound, IERC1155) onlyRole(SOCIAL_RECOVERY_ROLE) {
        _safeBatchTransferFrom(from, to, ids, amounts, data);
    }

    /**
     * @dev Mints an existing token to an address.
     * Only minters can call this function.
     */
    function mint(uint256 tokenId, address to) external onlyRole(MINTER_ROLE) {
        _requireNotStopped();
        require(_exists(tokenId), "Invalid token ID");
        _mint(to, tokenId, 1, "");
    }

    /**
     * @dev Mints an existing token to multiple addresses.
     * Only minters can call this function.
     */
    function mintToMany(uint256 tokenId, address[] memory to) external onlyRole(MINTER_ROLE) {
        _requireNotStopped();
        require(_exists(tokenId), "Invalid token ID");
        _mintToMany(tokenId, to);
    }

    /**
     * @dev Creates a new token and mints it to an addresses.
     * Only minters can call this function.
     */
    function createAndMint(address to, TokenData calldata data) external onlyRole(MINTER_ROLE) {
        _requireNotStopped();
        uint256 tokenId = ++tokenIdCounter;
        _create(tokenId, data);
        _mint(to, tokenId, 1, "");
    }

    /**
     * @dev Creates a new token and mints it to multiple addresses.
     * Only minters can call this function.
     */
    function createAndMintToMany(address[] memory to, TokenData calldata data) external onlyRole(MINTER_ROLE) {
        _requireNotStopped();
        uint256 tokenId = ++tokenIdCounter;
        _create(tokenId, data);
        _mintToMany(tokenId, to);
    }

    /**
     * Stops the contract. This can not be undone. Social recovery is still available after stop,
     * but no more tokens can be created or minted.
     */
    function stop() external onlyRole(TERMINATOR_ROLE) {
        stopped = true;
    }

    /**
     * @dev Mints a token to multiple addresses.
     * Private function without access restriction.
     */
    function _mintToMany(uint256 tokenId, address[] memory to) private {
        for (uint256 i = 0; i < to.length; ++i) {
            _mint(to[i], tokenId, 1, "");
        }
    }

    /**
     * @dev Creates a new token and sets its data.
     * Private function without access restriction.
     */
    function _create(uint256 id, TokenData calldata data) private {
        require(bytes(data.name).length > 0, "Empty name");
        tokenData[id] = data;
    }

    /**
     * @dev True if a token with this id has been created.
     */
    function _exists(uint256 tokenId) private view returns (bool) {
        return bytes(tokenData[tokenId].name).length > 0;
    }

    /**
     * @dev Throws if contract is stopped.
     */
    function _requireNotStopped() private view {
        require(!stopped, "Contract stopped");
    }
}
