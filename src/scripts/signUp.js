var API_URL="https://8stpnma0n7.execute-api.us-east-1.amazonaws.com/stg1/shubh";
		var temp=API_URL;
		$('#SignupButton').on('click',function(){
   			if($("#cusName").val()=='' || $("#password").val()=='' || $("#cusEmail").val()=='')
   			{
   				swal({
					title: "Incomplete Form",
					text: "Please enter Valid Details",
					icon: 'error'
				})
   			}
   			else
			{
				newUrl=API_URL+"?VoterName="+$("#cusName").val()+"&password="+$("#password").val()+"&VoterEmail="+$('#cusEmail').val();
                     	console.log(newUrl);
				$.ajax({
					type: 'GET' ,
					url:newUrl,
					success:function(data){
						console.log(data);
						var msg="Hi! "+$("#cusName").val()+", Your sign up was successfull and your Aadhar No. is-"+data.body['AadharNo'];
						if(data.body['passcode']==1){
							swal({
							title: msg,
							text: "Click Ok to enter the central Electoral Syatem",
							icon: "success",
							buttons: true,
							})
							.then((willLogin) => {
							if (willLogin) {
							//    var x = document.getElementById("assId");
								// x.value="1111";
								// console.log(x.value);
								location.replace("ClientDashboard.html");
							} else {
							swal("Taking you to the login page!");
							}
							});
						}  
						else{
							swap("Please enter valid details!")
						} 
					}
				});
                     API_URL=temp;
                     return false;
			}
      });
