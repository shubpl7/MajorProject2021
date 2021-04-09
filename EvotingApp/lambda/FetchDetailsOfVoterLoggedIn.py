import json
import boto3
from botocore.exceptions import ClientError
import random
# from boto3.dynamodb.conditions import Key, Attr
dbclient=boto3.resource('dynamodb')
class DatabaseInteraction:
    def __init__(self, tableName, PrimaryKey):
        self.tableName=tableName
        self.PrimaryKey=PrimaryKey
        
     
    def PutItem(self, TobePut):
        table=dbclient.Table(self.tableName)   
        response=table.put_item(
            Item=TobePut
        )
        return response
        
    def GetItem(self,key):
        table=dbclient.Table(self.tableName)
        response=table.get_item(
            Key={self.PrimaryKey: key}
        )
        return response
        
    def Update(self, key, AttributeName, newValue):
        table=dbclient.Table(self.tableName)
        UpdateString = "SET "+AttributeName+"=:val1"
        response=table.update_item(
            Key={self.PrimaryKey: key},
            UpdateExpression=UpdateString,
            ExpressionAttributeValues={
                ':val1': newValue
            }
        )
        return response
    
    def Delete(self, key):
        table=dbclient.Table(self.tableName)
        response=table.delete_item(
            Key={self.PrimaryKey:key}
        )
        return response
    def Scan(self):
        table=dbclient.Table(self.tableName)
        response=table.scan()
        return response
        

def lambda_handler(event, context):
    try:
        CusLogin = DatabaseInteraction('VoterLogin','AadharNo')
        response = CusLogin.Scan()
        if(len(response['Items'])==0):
            passcode=2 #voter not found
            VoterName = ''
            AadharNo = ''
        else:
            VoterName = response['Items'][0]['VoterName']
            AadharNo = response['Items'][0]['AadharNo']
            VoterTable = DatabaseInteraction('voters','AadharNo')
            response = VoterTable.GetItem(AadharNo)
            print(response)
            if(response['Item']['VoteStatus']=='true'):
                passcode=3 #voter has already casted vote
            else:
                passcode=1 #voter not casted vote
                # sending of OTP
                VoterEmail = response['Item']['VoterEmail']
                otp = str(random.randint(10000,90000));
                client2=boto3.client("ses")
                subject="""Hi {}! Please Verify yourself before Proceeding to Vote. """.format(VoterName)
                body="""
                <br>
                Dear {},<br>Your One Time Password(OTP), for the verification on central Voting System is {}.
                <br> Please enter it, on the E-voting application and proceed to Vote.
                This OTP will be valid for 10 min only.
                <br> Thanks, Have a nice day.
                """.format(VoterName,otp)
                message={"Subject":{"Data":subject},"Body":{"Html":{"Data":body}},}
                response1=client2.send_email(Source="shubhampalmanit@gmail.com",Destination={"ToAddresses":["shubhampalggps@gmail.com","dharmeshmanitcse@gmail.com"]},Message=message)
                # adding OTP to the voterLoginTable
                enterotp = DatabaseInteraction('OTPofCurrentLogin','OTP')
                OTPinfo = {
                    'OTP':otp
                }
                enterotp.PutItem(OTPinfo)
                
                
            print(passcode)
                
        return{
            'statusCode': 200,
            'body': {'passcode':passcode,'VoterName':VoterName,'AadharNo':AadharNo}
        
        }    
    except ClientError as e:
    # print(e.response['Error']['Code'])
        raise e
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
 