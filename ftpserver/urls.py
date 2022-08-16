from django.urls import path 
from .views import GETALLFILES, FTPUPLOAD
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("get-files",GETALLFILES),
     path("upload-files",FTPUPLOAD)
     #path("connect-server/", Connect,name='serverconnection'),
]


# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)