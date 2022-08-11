import boto3 
import json

def GetBucketSession():

    df = json.load(open("files/cred.json"))
    print(df['aws_access_key_id'],df['aws_secret_access_key'])
    session = boto3.Session(
        aws_access_key_id= str(df['aws_access_key_id']),
        aws_secret_access_key = str(df['aws_secret_access_key'])
        )
    s3 = session.resource('s3')

    return s3

# s3 = GetBucketSession(aws_access_key_id = 'AKIA5IM6XOLZSBR2ARR5', 
# ws_secret_access_key='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',)
