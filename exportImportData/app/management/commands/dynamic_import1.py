import pandas as pd
from django.apps import apps
from django.core.management.base import BaseCommand
from datetime import datetime
from employee_basic_information.models import *
import numpy as np
from phonenumbers import parse, is_valid_number

class Command(BaseCommand):
    help = 'Import data from a CSV file into a Django model'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        model_name = options['model_name']
        file_path = options['file_path']
        print("file_path ",file_path )
        # file_path = 'F:\TMRC_PLRA\PLRA\employee_basic_information_position.csv'

        model = apps.get_model('employee_basic_information', model_name)
        print(model)

        df = pd.read_csv(file_path, index_col=False, encoding='ISO-8859-1')
        print(df.head())
        print(df.dtypes)
        
        # df = df.drop(['Unnamed: 0', 'leave_type_id'], axis=1)
        headers= df.columns
        rows = df.replace({np.nan: None}).to_dict(orient='records')

        # Dynamically identify date fields from the model
        date_fields = [field.name for field in model._meta.get_fields() if isinstance(field, (models.DateField, models.DateTimeField))]

        # Convert those fields in the DataFrame to datetime.date
        # for date_field in date_fields:
        #     if date_field in df.columns:
        #         df[date_field] = pd.to_datetime(df[date_field]).dt.date

        def get_or_create_foreign_key(field, field_value):
            if field_value not in [None, '']:
                related_model = field.related_model
                primary_key_field = related_model._meta.pk.name

                # If the value is numeric, assume it's an ID and fetch the instance directly
                if isinstance(field_value, (int, float)):
                    try:
                        return related_model.objects.get(pk=field_value)
                    except related_model.DoesNotExist:
                        print(f"{related_model.__name__} with ID {field_value} does not exist.")
                        return None
                # If the value is a string, try to find the related instance by matching the string representation
                for related_instance in related_model.objects.all():
                    if related_instance.__str__().strip().lower() == str(field_value).strip().lower():
                        print(related_instance)
                        return related_instance
                # If the value is a string, try to find the related instance by matching a text field
                for related_field in related_model._meta.get_fields():
                    if isinstance(related_field, models.CharField):
                        try:
                            instance = related_model.objects.get(**{related_field.name: field_value})
                            return instance
                        except related_model.DoesNotExist:
                            continue  # Try the next field
                print(f"{related_model.__name__} with value '{field_value}' not found in any text field.")
                return None

            return None
        
        if 'phonenumber' in df.columns:
            df['phoneNumber'] = df['phoneNumber'].astype(str).replace('nan', '')
            df['phoneNumber'] = df['phoneNumber'].apply(lambda x: str(int(float(x))) if isinstance(x, float) and 'E' in str(x) else x)
            print("Phone numbers processed successfully.")
        else:
            print("Warning: 'phonenumber' column not found in the CSV, skipping processing for phone numbers.")
        # print('rows',rows)
        

        for row in rows:
            try:
                for field in model._meta.get_fields():
                    if field.is_relation and not field.many_to_many and field.name in row:
                        row[field.name] = get_or_create_foreign_key(field, row[field.name])

                for date_field in date_fields:
                    if date_field in row and row[date_field] is not None:
                        try:
                            # Convert the date string to a date object
                            row[date_field] = pd.to_datetime(row[date_field], errors='coerce').date()
                        except Exception as e:
                            print(f"Error converting {date_field} with value {row[date_field]} to date: {e}")
                            # row[date_field] = None 
                    
                    # Handle explicit type conversions based on field types
                    # if field.name in row:
                    #     if isinstance(field, models.CharField):
                    #         row[field.name] = str(row[field.name]) if row[field.name] is not None else None
                    #     elif isinstance(field, models.IntegerField):
                    #         row[field.name] = int(row[field.name]) if row[field.name] is not None else None
                    #     elif isinstance(field, models.FloatField):
                    #         row[field.name] = float(row[field.name]) if row[field.name] is not None else None

                if 'phoneNumber' in row and row['phoneNumber'] not in [None, '']:
                    phone_number_str = row['phoneNumber']
                    if isinstance(phone_number_str, float):
                        phone_number_str = str(int(phone_number_str))  # Convert float to string

                    parsed_number = parse(phone_number_str, "PK")
                    if is_valid_number(parsed_number):
                        row['phoneNumber'] = parsed_number
                    else:
                        print(f"Invalid phone number: {phone_number_str}")
                        continue


                rec=model.objects.update_or_create(**row)
                print(f"Record created: {rec}")
                print('Data imported successfully!')
            
            except Exception as e:  
                print(f"Error processing row: {row}. Error: {e}")

        

