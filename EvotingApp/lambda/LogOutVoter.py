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
        CusLoginTable = DatabaseInteraction('VoterLogin','AadharNo')
        response = CusLoginTable.Scan();
        deleteKey = response['Items'][0]['AadharNo']
        CusLoginTable.Delete(deleteKey)
        OTPTable = DatabaseInteraction('OTPofCurrentLogin','OTP')
        response1 = OTPTable.Scan();
        deleteKey1 = response1['Items'][0]['OTP']
        OTPTable.Delete(deleteKey1)
    except ClientError as e:
    # print(e.response['Error']['Code'])
        raise e
    return
 