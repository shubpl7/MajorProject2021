 pragma solidity ^0.4.21;
 contract elction{
     struct candidate{
        string name;
        uint votecnt;
     }
     struct voter{
         bool authorized;
         bool voted;
         uint vote;
     }
     address public owner;
     string public electionname;
     mapping(address => voter) public voters;
     candidate[] candidates;
     uint public totalvotes;
     
     modifier owneronly(){
         require(msg.sender==owner);
         _;
     }
     function election (string _name)public{
         owner = msg.sender;
         electionname =_name;
     }
     function addcandidate(string _name)owneronly public{
         candidates.push(candidate(_name, 0));
     }
     
     function getnumcandidate() public view returns(uint){
         return candidates.length;
     }
     function authorize(address _person)owneronly public{
         voters[_person].authorized=true;
     }
     function vot(uint _voteindex)public{
         require(!voters[msg.sender].voted);
         require(voters[msg.sender].authorized);
         voters[msg.sender].vote=_voteindex;
         voters[msg.sender].voted=true;
         totalvotes+=1;
     }
     function end() owneronly public{
         selfdestruct(owner);
     }
 }