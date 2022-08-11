
# import boto3

# #Creating Session With Boto3.
# session = boto3.Session(
# aws_access_key_id='AKIA5IM6XOLZSBR2ARR5',
# aws_secret_access_key='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'
# )

# #Creating S3 Resource From the Session.
# s3 = session.resource('s3')

# object = s3.Object('application-aws-version', 'media/file_name.txt')

# txt_data = b'This is the content of the file uploaded from python boto3'

# result = object.put(Body=txt_data)

# res = result.get('ResponseMetadata')

# if res.get('HTTPStatusCode') == 200:
#     print('File Uploaded Successfully')
# else:
#     print('File Not Uploaded')

# getobjects = s3.Bucket('application-aws-version')

# for objects in getobjects.objects.all():
#     print(objects.key)
import requests
import os 

dirs = os.listdir('media/')

files = {}
for i in dirs:
    files[i] = open("media/"+i,'rb')
# files = {'FILES': open('requirements.txt', 'rb'), 'file2': open('AppIcons.zip', 'rb')}
r = requests.post('http://127.0.0.1:8000/uplaoder/get-access', files=files)

print(r)