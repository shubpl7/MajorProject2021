import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
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
        
    def Query(self, key):
        table=dbclient.Table(self.tableName)
        response = table.query(
            KeyConditionExpression=Key(self.PrimaryKey).eq(key)
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
        VoterTable = DatabaseInteraction('voters','AadharNo')
        response = VoterTable.Query(event['AadharNo'])
        VoterName = ''
        print(response['Items']) 
        # print(len(response['Item']))
        if((len(response['Items']))==0):
            passcode = 1
            # No customer with given Cus Id exists
        else:
            VoterName = response['Items'][0]['VoterName']
            if(response['Items'][0]['password']==event['password']):
                passcode = 2
                # Password matched
                VoterLogin = DatabaseInteraction('VoterLogin','AadharNo')
                LoginInfo={
                    'AadharNo':event['AadharNo'],
                    'VoterName':VoterName
                }
                VoterLogin.PutItem(LoginInfo)
                
            else:
                passcode = 3
                #password not matched
        return {
            'statusCode': 200,
            'body': {'passcode':passcode,'VoterName':VoterName}
        }
        
    except ClientError as e:
        raise e
    