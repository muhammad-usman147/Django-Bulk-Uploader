from django.urls import path 
from .views import UploadFiles, GetAllFiles,DownloadFiles
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('upload-file',UploadFiles,name='uploadfiles'),
    path('get-all-files',GetAllFiles,name='GetAllFiles'),

    path('download-files/<filename>',DownloadFiles,name='DownloadFile')
]


# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)