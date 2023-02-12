#!/usr/bin/env python
# coding: utf-8

# In[5]:


from solcx import compile_source,install_solc
install_solc
compiled_sol=compile_source(
'''
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
'''
,output_values=['bin','abi']
)


# In[6]:


from web3 import Web3
contract_id,contract_interface=compiled_sol.popitem()
a=contract_interface['abi']
b=contract_interface['bin']
w3=Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
ballot=w3.eth.contract(abi=a,bytecode=b)


# In[7]:


tx_hash=ballot.constructor().transact()


# In[8]:


nonce=w3.eth.getTransactionCount("0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427")
tx1=ballot.constructor().buildTransaction(
{
    "gasPrice":w3.eth.gas_price,
    "from":"0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427",
    "nonce":nonce
})


# In[11]:


p="0x2f82a4a1160afd15db54f7e4fb74153f01c6e500a3570250c6e6bace1d198c37"
signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=p)


# In[13]:


tx_hash=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


# In[14]:


tx_recipt=tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)


# In[15]:


con_instance=w3.eth.contract(address=tx_recipt.contractAddress,abi=a)


# In[20]:


nonce=w3.eth.getTransactionCount("0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427")
tx2=con_instance.functions.register("0x1c53eBD8BA7096c643A3DF21496bd7ef94f82ea7").buildTransaction(
{
        "gasPrice":w3.eth.gas_price,
    "from":"0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427",
    "nonce":nonce
})
signed_tx=w3.eth.account.sign_transaction(tx2,private_key=p)
tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[21]:


nonce=w3.eth.getTransactionCount("0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427")
tx3=con_instance.functions.register("0x4735ADCDDEAcD59F486380b7a9D1ca47228F94f8").buildTransaction(
{
        "gasPrice":w3.eth.gas_price,
    "from":"0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427",
    "nonce":nonce
})
signed_tx=w3.eth.account.sign_transaction(tx3,private_key=p)
tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[25]:


nonce=w3.eth.getTransactionCount("0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427")
tx4=con_instance.functions.vote(1).buildTransaction(
{
        "gasPrice":w3.eth.gas_price,
    "from":"0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427",
    "nonce":nonce
})
signed_tx=w3.eth.account.sign_transaction(tx4,private_key=p)
tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[24]:


nonce=w3.eth.getTransactionCount("0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427")
tx4=con_instance.functions.change_state(2).buildTransaction(
{
        "gasPrice":w3.eth.gas_price,
    "from":"0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427",
    "nonce":nonce
})
signed_tx=w3.eth.account.sign_transaction(tx4,private_key=p)
tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[27]:


nonce=w3.eth.getTransactionCount("0x1c53eBD8BA7096c643A3DF21496bd7ef94f82ea7")
tx4=con_instance.functions.vote(1).buildTransaction(
{
        "gasPrice":w3.eth.gas_price,
    "from":"0x1c53eBD8BA7096c643A3DF21496bd7ef94f82ea7",
    "nonce":nonce
})
p="0x25e34777748703db0b353a1b6970f88a6ca6c99e31ca846d3cc9a3c3deacd4a0"
signed_tx=w3.eth.account.sign_transaction(tx4,private_key=p)
tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[33]:


con_instance.functions.winningProposal().call()


# In[32]:


nonce=w3.eth.getTransactionCount("0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427")
tx4=con_instance.functions.change_state(3).buildTransaction(
{
        "gasPrice":w3.eth.gas_price,
    "from":"0x71E5fFC8CE9110c72f6ed533b5D9c78854FD6427",
    "nonce":nonce
})
p="0x2f82a4a1160afd15db54f7e4fb74153f01c6e500a3570250c6e6bace1d198c37"
signed_tx=w3.eth.account.sign_transaction(tx4,private_key=p)
tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[ ]:




