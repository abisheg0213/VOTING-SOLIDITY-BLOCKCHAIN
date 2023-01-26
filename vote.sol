pragma solidity ^0.4.10;
contract ballot
{
    struct voter
    {
        uint weight;
        bool voted;
    }
    struct candidate
    {
        uint votecount;
        // string canname;
    }
    address chairperson;
    mapping (address => voter) Voter;
    candidate [] cans;
    address [] voters;
    // uint public v;
    function ballot(uint8 noofcandidates)
    {
        chairperson=msg.sender;
        cans.length=noofcandidates;
        Voter[msg.sender].weight=2;
        Voter[msg.sender].voted=false;
        voters.push(chairperson);
    }
    modifier onlyby(address s)
    {
        require(s==chairperson);
        _;
    }
    modifier vervoted(address h)
    {
        require(Voter[h].voted==false);
        _;
    }
    function register(address vt) public onlyby(msg.sender)
    {
        Voter[vt].weight=1;
        Voter[vt].voted=false;
        voters.push(vt);
    }
    function regvoter(address r) returns(bool)
    {
        uint y=0;
        bool avail;
        for(uint i=0;i<voters.length;i++)
        {
            // v=i;
            if(voters[i]==r)
            {
                avail=true;
                y=1;
            }
        }
        if (y==0)
        {
            avail=false;
        }
        return avail;
    }
    function vote(uint8 i) public vervoted(msg.sender) 
    {
        if(regvoter(msg.sender)==true)
        {
           cans[i].votecount+=Voter[msg.sender].weight;
           Voter[msg.sender].voted=true;
        }
        else
        {
            return;
        }
    }
    function winningProposal() constant public returns(uint8)
    {
        uint max=0;
        uint8 winp=0;
        for (uint8 j=0;j<cans.length;j++)
        {
            if (max<cans[j].votecount)
            {
                max=cans[j].votecount;
                winp=j;
            }
        }
        return winp;
    }
}
