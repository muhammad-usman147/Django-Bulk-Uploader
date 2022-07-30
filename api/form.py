from django import forms
from .models import ChurnData, CsvData
from django.contrib.auth import get_user_model


class CsvForm(forms.ModelForm):

    class Meta:
        model = CsvData
        fields = ['dataset']

class ChurnForm(forms.ModelForm):

    class Meta:
        model = ChurnData
        fields = ['filename', 'imageFile']
