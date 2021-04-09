var API_URL="https://5ojy4a2knl.execute-api.us-east-1.amazonaws.com/stg1/shubh";
var temp=API_URL;
$(document).ready(function(){
     let a=document.getElementById("intro")
     $.ajax({
            type: 'GET' ,
            url:API_URL,
            success:function(data){
                   if(data.body['passcode']==1)
                   {
                          var msg="Hi "+data.body['VoterName']+"! ,You are succesfully logged in";
                          swal({
                            title: msg,
                            text: "Please Check your Email for the OTP, and proceed for verification",
                            icon: "success",
                            })
                            let a=document.getElementById('intro');
                            a.innerHTML="Hi "+data.body['VoterName']+"! Welcome to the Central Electoral System";
                            
                   }
                   else if(data.body['passcode']==2)
                   {
                          var msg="Sorry you are not logged in please login first";
                          swal({
                            title: msg,
                            text: "taking you to the login page",
                            icon: "error",
                            button: true,
                            })
                            .then((willLogin) => {
                            if (willLogin) {
                                   location.replace("loginPage.html");
                            }
                            });
                   }
                   else if(data.body['passcode']==3)
                   {
                            var msg="Hey, you have already casted your Vote";
                            swal({
                            title: msg,
                            text: "Logging you out",
                            icon: "error",
                            button: true,
                            })
                            .then((willLogin) => {
                            if (willLogin) {
                                   var logoutURL = "https://2thnr61wdb.execute-api.us-east-1.amazonaws.com/stg1/shubh";
                                   $.ajax({
                                          type: 'GET' ,
                                          url:logoutURL,
                                          success:function(data){
                                             console.log(data);
                                             swal({
                                                    title: "You have successfully logged out!",
                                                    text: "Click ok",
                                                    icon: "success",
                                                    button :true,
                                                    })
                                                    .then((willLogin) => {
                                                           if (willLogin) {
                                                                  location.replace("loginPage.html");
                                                           }
                                                    });
                                                 
                                          }
                                   });
                            }
                            });
                   }
               
            }
           
     });
     return false;
});
var logoutURL="https://2thnr61wdb.execute-api.us-east-1.amazonaws.com/stg1/shubh";
$('#logout').on('click',function(){
           // console.log(newUrl);
           $.ajax({
                  type: 'GET' ,
                  url:logoutURL,
                  success:function(data){
                     console.log(data);
                     swal({
                            title: "You have successfully logged out!",
                            text: "Click ok",
                            icon: "success",
                            button :true,
                            })
                            .then((willLogin) => {
                                   if (willLogin) {
                                          location.replace("loginPage.html");
                                   }
                            });
                         
                  }
           });
    return false;
    }
);

var OTPurl = "https://0gavqtvq48.execute-api.us-east-1.amazonaws.com/stg1/shubh";
$('#loginButton').on('click',function(){
              // console.log(newUrl);
              newUrl=OTPurl+"?otp="+$("#cusId").val();
		$.ajax({
			type: 'GET',
			url:newUrl,
			success:function(data){
				console.log(data);
				
				if(data.body['passcode']==1){
					// correct OTP
					swal({
					title: "Your OTP verification is Successfull!",
					text: "Please proceed to Vote",
                                   icon: "success",
                                   button :true,

                                   })
                                   .then((willLogin) => {
                                          if (willLogin) {
                                                 var VoteURL = "https://tmilhpt21d.execute-api.us-east-1.amazonaws.com/stg1/shubh";
                                                 $.ajax({
                                                        type: 'GET' ,
                                                        url:VoteURL,
                                                        success:function(data){
                                                               console.log(data);
                                                               swal({
                                                                      title: "You are now moving to the Block-chain based voting system!",
                                                                      text: "Click ok",
                                                                      icon: "success",
                                                                      button :true,
                                                                      })
                                                                      .then((willLogin) => {
                                                                             if (willLogin) {
                                                                                    location.replace("index.html");
                                                                             }
                                                                      });
                                                                   
                                                            }
                                                 });
                                                 
                                          }
                                   });
					
				}  
				else{
                                   // wrong OTP
					swal({
                                          title: "Your OTP is Wrong!",
                                          text: "please Enter the correct OTP",
                                          icon: "error",
                            })
                            }
			}
		});
	return false;
	
});
