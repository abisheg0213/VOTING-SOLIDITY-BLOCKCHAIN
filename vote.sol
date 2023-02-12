pragma solidity ^0.8.14;
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
    enum Stage{init,reg,vote,done}
    Stage public stage=Stage.init;
    address chairperson;
    mapping (address => voter) Voter;
    candidate [3] cans;
    address [] voters;

    constructor()
    {
        chairperson=msg.sender;
        stage=Stage.reg;
        // cans=new candidate[](noofcandidates);
        Voter[msg.sender].weight=2;
        Voter[msg.sender].voted=false;
        voters.push(chairperson);
      
    }
    function change_state(uint k) public onlyby(msg.sender){
        if (k==2)
        {
            stage=Stage.vote;
        }
        if(k==3)
        {
            stage=Stage.done;
        }
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
    modifier reqstage(Stage t)
    {
        require(stage==t);
        _;
    }
    function register(address vt) public onlyby(msg.sender) reqstage(Stage.reg)
    {
        Voter[vt].weight=1;
        Voter[vt].voted=false;
        voters.push(vt);
       
    }
    modifier bvalvoter(address h)
    {
        require(regvoter(h)==true);
        _;
    }
    function regvoter(address r) public returns(bool)
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
    function vote(uint8 i) public vervoted(msg.sender) reqstage(Stage.vote) bvalvoter(msg.sender)
    {
           cans[i].votecount+=Voter[msg.sender].weight;
           Voter[msg.sender].voted=true;
    }
    function winningProposal() view public reqstage(Stage.done) returns(uint8)
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
