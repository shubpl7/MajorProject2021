import json
import boto3
import random
from botocore.exceptions import ClientError
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
        Customer = DatabaseInteraction('voters','AadharNo')
        response = Customer.Scan()
        AadharNo = str((random.randint(1,100))*len(response['Items'])+1000)
        SignUpInfo = {
        'AadharNo':AadharNo,
        'VoterName':event['VoterName'],
        'password':event['password'],
        'VoterEmail':event['VoterEmail'],
        'VoteStatus':'false'
        }
        LoginInfo = {
            'AadharNo':AadharNo,
            'VoterName':event['VoterName']
        }
        Customer.PutItem(SignUpInfo)
        
        CustomerLoginTable = DatabaseInteraction('VoterLogin','AadharNo')
        CustomerLoginTable.PutItem(LoginInfo)
        return{
            'statusCode': 200,
            'body': {'passcode':1,'AadharNo':AadharNo}
        }
    except ClientError as e:
    # print(e.response['Error']['Code'])
        raise e
        return{
            'statusCode': 200,
            'body': {'passcode':2,'AadharNo':AadharNo}
        }
        # raise e
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    
    
    
