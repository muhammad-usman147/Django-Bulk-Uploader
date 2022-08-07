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
        for name in request.FILES.items():
            print(str(name[1]))
            with open("media/"+str(name[1]),'wb') as f:
                f.write(name[1].read())

        return JsonResponse({"msg":"True"})


    
