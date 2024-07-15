// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Ye_Sheng_Qiao_Mu_Sheng_Bing is ERC721URIStorage, ReentrancyGuard, Ownable {
    uint256 public _totalSuply;

    mapping(address => bool) public _isMinter;

    modifier onlyMinter() {
        require(_isMinter[msg.sender], "!Minter");
        _;
    }

    constructor() ERC721("Ye_Sheng_Qiao_Mu_Sheng_Bing","TEA") Ownable(msg.sender) {
        _isMinter[msg.sender] = true;
    }

    function setMinter(address _address, bool _status) public onlyOwner() {
        _isMinter[_address] = _status;
    }

    function mint(address _to, uint256 _tokenId, string memory _tokenURI) public onlyMinter { 
        _mint(_to, _tokenId);
	    _setTokenURI(_tokenId, _tokenURI);
        _totalSuply += 1;
    } 

    function multimint (address[] memory _dests, uint256[] memory _tokenIds, string[] memory _tokenURIs) public onlyMinter returns (uint256) {
        uint256 i = 0;
        while (i < _dests.length) {
            mint(_dests[i], _tokenIds[i], _tokenURIs[i]);
            i += 1;
        }
        return(i);
    }

    function burn(uint256 _tokenId) public {
        require(msg.sender == _ownerOf(_tokenId), "Access of non-owner address");
        _update(address(0), _tokenId, _msgSender());
    }
}
