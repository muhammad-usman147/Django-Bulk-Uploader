from django.db import models

# Create your models here.
class UserFiles(models.Model):
    userfile = models.FileField( null=True)