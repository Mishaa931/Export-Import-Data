from django.db import models

class CSVFileUpload(models.Model):
    model_name=models.CharField(max_length=50)
    file=models.FileField(upload_to="CSV")
