from pyexpat import model

from pyrsistent import field
from rest_framework import serializers
from .models import CsvData
from .models import ChurnData


class CsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvData
        fields = ['id', 'dataset', 'dataset_name']

class ChurnDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurnData
        fields = ['filename', 'imageFile']
