import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Job, Ppg_Level_Setup

class Command(BaseCommand):
    help = 'Import jobs from a CSV file into the Job model'

    def handle(self, *args, **kwargs):
        file_path = 'F:\TMRC_PLRA\PLRA\employee_basic_information_job.csv'
        df = pd.read_csv(file_path)
        df.head()

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            # Fetch the Ppg_Level_Setup instance based on the ppg_level value from the CSV
            try:
                ppg_level = Ppg_Level_Setup.objects.get(ppg_level=row['ppg_level'])
                print("ppg_level",ppg_level)
            except Ppg_Level_Setup.DoesNotExist:
                print("error")
                continue
           
            job, created = Job.objects.update_or_create(
                job_id=row['job_id'],
                defaults={
                    'job_title': row['job_title'],
                    'job_abbrivation': row.get('job_abbrivation'),
                    'no_of_seniority_level': row.get('no_of_seniority_level', 1),
                    'ppg_level': ppg_level,
                    'full_time_equivalent': row.get('full_time_equivalent', Job.FULL_TIME_EQUIVALENT),
                    'maximum_number_of_positions': row.get('maximum_number_of_positions', Job.MAXIMUM_NUMBER_OF_POSITIONS),
                }
            )
            print("imported!")

            
        
