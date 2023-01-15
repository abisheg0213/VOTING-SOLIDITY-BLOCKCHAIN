pragma solidity ^0.4.0;
contract ballot
{
struct voter
{
    uint8 weight;
    bool voted;
    uint8 vote;
}
struct candidate
{
    uint8 votecount;
}
address chperson;
mapping (address => voter) voters;
candidate [] c;
function ballot(uint8 noofcan) public
{
    chperson=msg.sender;
    voters[msg.sender].weight=2;
    c.length=noofcan;
}
function register(address v) public
{
    if (msg.sender!=chperson)
    {
        return;
    }
    else{
        voters[v].voted=false;
        voters[v].weight=1;
    }
}
function vote(uint8 proposal) public
{
    voter g=voters[msg.sender];
    if (g.voted=true || proposal >= c.length)
    {
        return;
    }
    else{
        c[proposal].votecount+=g.weight;
        voters[msg.sender].voted=true;
    }
}
function winningProposal() public constant returns(uint8)
{
    uint8 wincount=0;
    uint winprop=0;
    for (uint8 p=0;p < c.length;p++)
    {
        if (wincount<c[p].votecount)
        {
            wincount=c[p].votecount;
            winprop=p;
        }
    }
    return p;
}

}
