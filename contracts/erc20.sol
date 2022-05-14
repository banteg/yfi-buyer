/// erc20.sol -- API for the ERC20 token standard

// See <https://github.com/ethereum/EIPs/issues/20>.

// This file likely does not meet the threshold of originality
// required for copyright to apply.  As a result, this is free and
// unencumbered software belonging to the public domain.

pragma solidity >0.4.20;

contract ERC20Events {
    event Approval(address indexed src, address indexed guy, uint wad);
    event Transfer(address indexed src, address indexed dst, uint wad);
}

abstract contract ERC20 is ERC20Events {
    function totalSupply() public virtual view returns (uint);
    function balanceOf(address guy) public virtual view returns (uint);
    function allowance(address src, address guy) public virtual view returns (uint);

    function approve(address guy, uint wad) public virtual returns (bool);
    function transfer(address dst, uint wad) public virtual returns (bool);
    function transferFrom( address src, address dst, uint wad) public virtual returns (bool);
}
