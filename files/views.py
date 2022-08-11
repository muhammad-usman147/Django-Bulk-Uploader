from http.client import HTTPResponse
from msilib.schema import File
from django.shortcuts import render, HttpResponse
from django.http.response import  JsonResponse
from .forms import UploadFileForm
import os
from .models import UserFiles
from django.core.files.storage import FileSystemStorage
import json 
import boto3
from django.utils.decorators import  method_decorator
from django.views.decorators.csrf import csrf_exempt
from .bucket import GetBucketSession
# Create your views here.

def UploadFiles(request): #manually
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        file = request.FILES.getlist('file')


        for f in file:
            print("xx"*10)
            print(f.name)
            uploadhandler(f)
        return render(request,'FileSection/upload.html', {"form":form})
    else:
        form = UploadFileForm()
    return render(request,'FileSection/upload.html', {"form":form})

def uploadhandler(f):
    with open(f'uploaded/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def GetAllFiles(request):
    if request.method=='GET':
        dirs = os.listdir('uploaded/')
        files_list = {
            'files':dirs
        }
        return render(request,'FileSection/FileView.html',files_list)
        
def DownloadFiles(request,filename):
    with open(f'uploaded/{filename}','rb') as reader:
        data = reader.read()
    response = HttpResponse(data, headers={
        'Content-Type':'application/octet-stream',
        'Content-Disposition':f'attachment; filename="{filename}"'
    })# content_type='application/admin-upload')
   
    return response

@method_decorator(csrf_exempt,name = 'dispatch')
def GetCred(request):
    if request.method == 'POST':
        print("-----------------------")
        s3 = GetBucketSession()
        print(request.FILES)
        print(request.headers)
        resposnes = {}
        for name in request.FILES.items():
            print("media/"+str(name[1]))
            objects = s3.Object('application-aws-version','media/'+str(name[1]))
            result = objects.put(Body = name[1].read())
            resposnes[str(name[1])] = 200
            
     
            


    
        return JsonResponse({"msg":str(resposnes)})



@method_decorator(csrf_exempt, name = 'dispatch')
def BotoGetFileNames(request):

    s3 = GetBucketSession()
    
    bucket = s3.Bucket('application-aws-version')
    files = {'Media_Files':[]}
    for obj in bucket.objects.all():
        x = obj.key
        if x.startswith('media/'):
            files['Media_Files'].append(obj.key)



    return JsonResponse({
        "MSG":str(files)
    })


@method_decorator(csrf_exempt, name = 'dispatch')
def Credentials(request):


    if request.method == "POST":


        access_key = request.POST.get("access-key")
        secred_key = request.POST.get("secred-key")

        df = json.load(open("files/cred.json"))
        print(access_key,secred_key)
        df['aws_access_key_id'] = access_key
        df['aws_secret_access_key'] = secred_key
        json_object = json.dumps(df)
        # Writing to sample.json
        with open("files/cred.json", "w") as outfile:
            outfile.write(json_object)
        return JsonResponse({
            "MSG":str("SAVED SUCCESSFULLY")
        })
    else:
        return JsonResponse({
            "ERROR":"INVALID METHOD"
        })