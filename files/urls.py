from django.urls import path 
from .views import UploadFiles, GetAllFiles,Credentials, DownloadFiles, GetCred, BotoGetFileNames
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload-file',UploadFiles,name='uploadfiles'),
    
    #path('get-all-files',GetAllFiles,name='GetAllFiles'),
    path('upload-files',GetCred,name='GetAllFiles'),
    path('download-files/<filename>',DownloadFiles,name='DownloadFile'),
    path("get-files",BotoGetFileNames,name='getcred'),
    path("upload-credentials",Credentials,name='getcred')
]


# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)