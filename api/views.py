from distutils.command.config import config
from fileinput import filename
from http.client import HTTPResponse
from tkinter import Image
from wsgiref.util import FileWrapper
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from api.custom_renderers import JPEGRenderer, PNGRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChurnDataSerializer, CsvSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .form import CsvForm
from .models import ChurnData, CsvData
import pandas as pd
from django.contrib.auth import settings
from .cgs_main import getData
from .cga_main import getCGAData
from .churn_main import getChurnData
import csv
import json
import boto3
from botocore.config import Config
import os
import io

from api import serializers


my_config = Config(
    signature_version = 's3v4',
)

USER = get_user_model()
aws_id = settings.AWS_ACCESS_KEY_ID
aws_secret = settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret, config=my_config)
bucket = 'application-aws-version'

# @api_view()
@permission_classes((AllowAny, ))
class list_of_data_view(viewsets.ModelViewSet):
    
    queryset = CsvData.objects.all()
    serializer_class = CsvSerializer
    
    @permission_classes((AllowAny, ))
    def create(self, request, *args, **kwargs):
        CsvData.objects.get_or_create(
            dataset = request.FILES.get('dataset'),
            dataset_name = str(request.FILES.get('dataset'))[:-4]
        )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        query = self.get_queryset()
        query.get(pk=pk).delete()
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        dataset = get_object_or_404(queryset, pk=pk)
        file_path = str(dataset.dataset)
        obj = s3.get_object(Bucket=bucket, Key=file_path)
        body = obj['Body']
        try:
            csv_content = body.read().decode('latin1').splitlines()  # "ISO-8859-1 utf-8
        except Exception as e:
            print(e)
            csv_content = body.read().decode('ISO-8859-1').splitlines()
        csv_data = csv.DictReader(csv_content)
        json_data = []
        for csv_row in csv_data:
            json_data.append(csv_row)
        jsonString = json.dumps(json_data)
        data = pd.read_json(jsonString)
        data.head()
        print(list(data.columns))
        return Response({
            'columns': list(data.columns)
        })
        
# @api_view()
# @permission_classes((IsAuthenticated, ))
@csrf_exempt
def result_api_view(request):
    all_data = json.loads(request.body)
    json_data, error_list, Warning_list = getData(all_data)

    return JsonResponse({
        "data" :json.loads(json_data),
        "warning": Warning_list,
        "error": error_list,
        "dataset_deleted": all_data['delete']
    }, safe=False)

@csrf_exempt
def result_cga_api_view(request):
    all_data = json.loads(request.body)
    json_data, error_list, Warning_list = getCGAData(all_data)

    return JsonResponse({
        "data" :json.loads(json_data),
        "warning": Warning_list,
        "error": error_list,
        "dataset_deleted": all_data['delete']
    }, safe=False)

@csrf_exempt
def result_churn_api_view(request):
    all_data = json.loads(request.body)
    json_data, error_list, Warning_list = getChurnData(all_data)

    return JsonResponse({
        "data" :json.loads(json_data),
        "warning": Warning_list,
        "error": error_list,
        "dataset_deleted": all_data['delete']
    }, safe=False)

@csrf_exempt
def get_churn_image(request):
        queryset = ChurnData.objects.all()
        imageSet = get_object_or_404(queryset, filename='chip-2.png')
        file_path = 'post_imags/'+str(imageSet.filename)

        url = s3.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': bucket,
                                    'Key': file_path,
                                },                                  
                                ExpiresIn=10)

        JsonResponse({
            "data" :url
        }, safe=False)


@permission_classes((AllowAny, ))
class ChurnDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        churn_data = ChurnData.objects.all()
        serializer = ChurnDataSerializer(churn_data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        churn_data_serializer = ChurnDataSerializer(data=request.data)
        if churn_data_serializer.is_valid():
            churn_data_serializer.save()
            return Response(churn_data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', churn_data_serializer.errors)
            return Response(churn_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)