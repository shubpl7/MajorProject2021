var API_URL="https://4z03fcl9oi.execute-api.us-east-1.amazonaws.com/stg1/shubh";
var temp=API_URL;
$('#loginButton').on('click',function(){
	if($("#cusId").val()=='' || $("#password").val()=='')
	{
		swal({
			title: "Incomplete Form",
			text: "Please enter Valid Details",
			icon: 'error'
		})
	}
	else
	{
		newUrl=API_URL+"?AadharNo="+$("#cusId").val()+"&password="+$("#password").val();
		// console.log(newUrl);
		$.ajax({
			type: 'GET' ,
			url:newUrl,
			success:function(data){
				console.log(data);
				
				if(data.body['passcode']==1){
					swal({
					title: "No Voter with Aadhar No. "+$("#cusId").val()+" exists",
					text: "please enter correct Aadhar No.",
					icon: "error",
					})
					
				}  
				else if(data.body['passcode']==2){
					var cusName=data.body['VoterName']
					var msg="Hi! "+cusName+", Your sign in was successfull";
					swal({
					title: msg,
					text: "Click ok to enter your dashboard",
					icon: "success",
					button :true,
					})
					.then((willLogin) => {
						if (willLogin) {
							location.replace("ClientDashboard.html");
						}
					});
					
				} 
				else{
					var cusName=data.body['VoterName']
					var msg="Hi! "+cusName+", Your password is wrong";
					swal({
					title: msg,
					text: "please enter correct password",
					icon: "error",
					})
					
				} 
			}
		});
	API_URL=temp;
	return false;
	}
});
$('#SignupButton').on('click',function(){
	location.replace("signUp.html");
	return false;
});

