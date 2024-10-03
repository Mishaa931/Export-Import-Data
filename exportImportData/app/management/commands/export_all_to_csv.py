import csv
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Export all tables to CSV files'

    def handle(self, *args, **options):
        # Get all models from all installed apps
        app_models = apps.get_models()
        
        for model in app_models:
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            file_name = f'{app_label}_{model_name}.csv'

            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                headers = [field.name for field in model._meta.fields]
                writer.writerow(headers)
                
                # Identify primary key field
                pk_field = model._meta.pk.name

                # Write data rows
                for obj in model.objects.all():
                    row = [getattr(obj, field) for field in headers]
                    writer.writerow(row)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported {model_name} to {file_name}'))
444