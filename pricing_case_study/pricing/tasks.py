from celery import shared_task
import csv
from .models import PriceData

@shared_task
def process_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)