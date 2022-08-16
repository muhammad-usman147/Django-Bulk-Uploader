from django.shortcuts import render
from django.http import JsonResponse
import ftplib

from django.utils.decorators import  method_decorator
from django.views.decorators.csrf import csrf_exempt

def GETALLFILES(request):
    try:
        if request.method == 'GET':
            host = 'localhost'
            ftport = 21
            ftpusername = 'mahad'
            password = 'abc123'

            ftp = ftplib.FTP(timeout=30)

            ftp.connect(host,ftport)

            ftp.login(ftpusername,password)

            response = {"FILES": []}
            for files in ftp.nlst():
                response['FILES'].append(files)
            ftp.quit()
            return JsonResponse(response)

        else:
            return JsonResponse({
                "MSG":"ERROR"
            })
    except Exception as e:
        return JsonResponse({
            "ERROR":str(e)
        })

@method_decorator(csrf_exempt,name = 'dispatch')
def FTPUPLOAD(request):
    if request.method == 'POST':
        host = 'localhost'
        ftport = 21
        ftpusername = 'mahad'
        password = 'abc123'
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(host,ftport)
        ftp.login(ftpusername,password)

        print("-----------------------")
        print(request.FILES)
        print(request.headers)
        resposnes = {}
        for name in request.FILES.items():
            print("media/"+str(name[1]))
            ftp.storbinary("STOR "+str(name[1]),  name[1]) 
            resposnes[str(name[1])] = 200
        
        ftp.quit()
        
     
            


    
        return JsonResponse({"msg":str(resposnes)})

