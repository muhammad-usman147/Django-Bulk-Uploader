from django.contrib import admin
from .models import CsvData
from .models import ChurnData

admin.site.register(CsvData)
admin.site.register(ChurnData)
