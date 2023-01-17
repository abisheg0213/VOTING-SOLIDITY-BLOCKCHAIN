pragma solidity ^0.4.10;
contract ballot
{
    struct voter
    {
        uint8 weight;
        bool voted;
    }
    address chairperson;
    mapping (address => voter) Voters;
    enum Stage{init,reg,vote,done}
    Stage public stage=Stage.init;
    uint public starttime;
    struct proposal
    {
        uint8 votecount;
    }
    proposal [] candidate;
    function ballot(uint8 noofprop)
    {
        chairperson=msg.sender;
        candidate.length=noofprop;
        Voters[msg.sender].weight=2;
        stage=Stage.reg;
        starttime=now;
    }
    modifier validstate(Stage vstate)
    {
        require(stage == vstate);
        _;
    }
    function register(address reg) public validstate(Stage.reg)
    {
        if (msg.sender!=chairperson)
        {
            return;
        }
        else
        {
            Voters[reg].weight=1;
            Voters[reg].voted=false;
        }
        if (now > (starttime+ 20 seconds)){
            stage=Stage.vote;
            starttime=now;
        }
    }
    function vote(uint8 prop) public validstate(Stage.vote)
    {
        if (Voters[msg.sender].voted==true)
        {
            return;
        }
        else
        {
            candidate[prop].votecount+=Voters[msg.sender].weight;
            Voters[msg.sender].voted=true;
        }
                if (now > (starttime+ 20 seconds)){
            stage=Stage.done;
            starttime=now;
        }
    }
    function winningProposal() constant public validstate(Stage.done) returns(uint8)
    {
        uint8 max=0;
        uint8 winp=0;
        for (uint8 j=0;j<candidate.length;j++)
        {
            if (max<candidate[j].votecount)
            {
                max=candidate[j].votecount;
                winp=j;
            }
        }
        return winp;
    }
}
