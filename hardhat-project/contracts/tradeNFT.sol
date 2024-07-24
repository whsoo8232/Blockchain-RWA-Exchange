// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract tradeNFT is ReentrancyGuard, Ownable {
    IERC20 public USDT;
    IERC721 public NFTs;
    address public NFT_owner;

    mapping(address => bool) public _isMinter;

    // NFT contract distribute
    address public _NFTs = 0x12e030CCaB2cc841E4b66e89f46D433F8bF6FA8E;
    address public _NFT_owner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    // token contracts distribute
    address public _USDT = 0xc0adb3cA9c756D5C12d08CF5FD8168d088A9E46d;


    event Trade_NFT_With_ETH(uint id, address user, uint tokenId, uint NFT_price);
    event Trade_NFT_With_USDT(uint id, address user, uint tokenId, uint NFT_price);
    event Withdraw_ETH(address user, uint amount);
    event Withdraw_USDT(address user, uint amount);


    constructor() Ownable(msg.sender) {
        USDT = IERC20(_USDT);
        NFTs = IERC721(_NFTs);
        NFT_owner = _NFT_owner;
    }


    function contract_ETH_balance() external view returns (uint256) {
        return address(this).balance;
    }

    function contract_USDT_balance() external view returns (uint256) {
        return USDT.balanceOf(address(this));
    }    

    function trade_NFT_with_ETH(uint256 id, uint256 tokenId, uint256 tokenPrice) external payable {
        require(NFTs.ownerOf(tokenId) == NFT_owner, "NFT does not exist in the list");
        require(NFTs.getApproved(tokenId) == address(this), "NFT has not been approved to contact");
        NFTs.transferFrom(NFT_owner, msg.sender, tokenId);
        emit Trade_NFT_With_ETH(id, msg.sender, tokenId, tokenPrice);
    }

    function trade_NFT_with_USDT(uint256 id, uint256 tokenId, uint256 tokenPrice) external payable {
        require(NFTs.ownerOf(tokenId) == NFT_owner, "NFT does not exist in the list");
        require(NFTs.getApproved(tokenId) == address(this), "NFT has not been approved to contact");
        require(USDT.allowance(msg.sender, address(this)) >= tokenPrice, "Approved token amount is not enough");
        require(USDT.transferFrom(msg.sender, address(this), tokenPrice), "USDT transfer failed");
        NFTs.transferFrom(NFT_owner, msg.sender, tokenId);
        emit Trade_NFT_With_USDT(id, msg.sender, tokenId, tokenPrice);
    }

    function withdraw_ETH() external onlyOwner {
        uint256 contractBalance = address(this).balance;
        payable(msg.sender).transfer(address(this).balance);
        emit Withdraw_ETH(msg.sender, contractBalance);
    }

    function withdraw_USDT() external onlyOwner {
        uint256 contractBalance = USDT.balanceOf(address(this));
        require(USDT.transfer(msg.sender, USDT.balanceOf(address(this))), "balance transfer failed");
        emit Withdraw_USDT(msg.sender, contractBalance);
    }
}