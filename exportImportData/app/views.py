from django.shortcuts import render
from django.core.management import call_command
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response

class CSVFileUploadAPIView(APIView):
    def post(self, request):
        serializer = CSVFileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            upload_file = serializer.save()
            call_command('employeeimport', upload_file.model_name, upload_file.file.path)
        
        return Response("Imported")

