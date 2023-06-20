// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyToken {
    struct Token {
        string name;
        uint256 totalSupply;
    }
    
    mapping(address => mapping(string => uint256)) public balanceOf;
    mapping(string => Token) public tokens;
    string[] public tokenNames;
    
    event Transfer(address indexed from, address indexed to, string tokenName, uint256 value);
    event Consume(address indexed to, string tokenName, uint256 value);
    event TokenAdded(string tokenName, uint256 tokenSupply);

    constructor() {}

    function addToken(string memory _tokenName, uint256 _tokenSupply) public {
        require(tokens[_tokenName].totalSupply == 0, "Token already exists");
        tokens[_tokenName] = Token(_tokenName, _tokenSupply);
        tokenNames.push(_tokenName);
        balanceOf[msg.sender][_tokenName] = _tokenSupply;
        emit TokenAdded(_tokenName, _tokenSupply);
    }

    function transfer(address _from, address _to, string memory _tokenName, uint256 _value) public returns (bool) {
        require(balanceOf[_from][_tokenName] >= _value, "Insufficient balance");
        balanceOf[_from][_tokenName] -= _value;
        balanceOf[_to][_tokenName] += _value;
        emit Transfer(_from, _to, _tokenName, _value);
        return true;
    }

    function consume(address _addr, string memory _tokenName, uint256 _value) public returns (bool) {
        require(balanceOf[_addr][_tokenName] >= _value, "Insufficient balance");
        balanceOf[_addr][_tokenName] -= _value;
        tokens[_tokenName].totalSupply -= _value;
        emit Consume(_addr, _tokenName, _value);
        return true;
    }
}
