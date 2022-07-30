from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class CsvData(models.Model):
    # user = models.ForeignKey(USER, on_delete=models.CASCADE)
    dataset = models.FileField(upload_to='datasets')
    dataset_name = models.CharField(max_length=70)
    # json_result = models.TextField(null=True, blank=True)
    # csv_result = models.FileField(upload_to='results', null=True, blank=True)

    def __str__(self):
        return self.dataset_name
    
class ChurnData(models.Model):
    filename = models.CharField(max_length=100)
    imageFile = models.ImageField(upload_to='post_imags')

    def __str__(self):
        return self.filename