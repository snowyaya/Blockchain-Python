// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // factory contract
    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    // mint new nfts based off this pug

    // create a new nft, is just mapping a tokenId to a new address/owner
    function createCollectible() public returns (uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
