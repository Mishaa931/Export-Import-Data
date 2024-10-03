from rest_framework import serializers
from .models import*
class CSVFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=CSVFileUpload
        fields='__all__'