# Export Import Data Management

**Export Import Data Management** is a Django-based project designed to facilitate the import and export of data between CSV files and Django models. This project includes management commands for exporting data from all tables to CSV files and dynamically importing data from a specified CSV file into designated Django models.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Management Commands](#management-commands)
- [API Endpoints](#api-endpoints)
- [Models](#models)



## Features

- **Export Data**: Export all tables in the Django project to CSV files with a simple management command.
- **Dynamic Import**: Import data from CSV files into specific Django models dynamically based on the provided model name.
- **Phone Number Validation**: Validate phone numbers using the `phonenumbers` library during the import process.
- **Error Handling**: Comprehensive error handling during the import process to ensure data integrity.
- **Django REST Framework**: Provide an API endpoint for uploading CSV files for import.

## Installation

To get started with the **Export Import Data Management** project, follow these steps:

1. **Clone the repository**:

       git clone https://github.com/Mishaa931/Export-Import-Data.git
       cd Export-Import-Data

2. Install required dependencies:

Make sure you have Python and pip installed. Then install the necessary packages:

    pip install -r requirements.txt
    
### Run Migrations:

Ensure the database is set up with the necessary models:

    python manage.py makemigrations
    python manage.py migrate

## Usage

### Management Commands

**Export Data**: To export all tables to CSV files, run the following command:

    python manage.py export

This will generate CSV files named {app_label}_{model_name}.csv for each model in the installed apps.

**Import Data**: To import data from a CSV file into a specified Django model, use the following command:

    python manage.py dynamic_import <model_name> <file_path>

Replace <model_name> with the name of the model you want to import data into, and <file_path> with the path to your CSV file.

## API Endpoints
**CSV File Upload**: This API endpoint allows for uploading CSV files for import. It uses the Django REST framework.

POST /import-data/
Request body should contain the model name and the file.

**Example request**:

    {
        "model_name": "your_model_name",
        "file": "path/to/your/file.csv"
    }

## Models
## CSVFileUpload Model
The CSVFileUpload model is used to handle the uploaded CSV files. It contains the following fields:

* model_name: The name of the model to which the data will be imported.
* file: The uploaded CSV file.

