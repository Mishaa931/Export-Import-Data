from django.urls import path,include
from .views import *
urlpatterns = [
    path('import_data/', CSVFileUploadAPIView.as_view(), name='import_data'),
]