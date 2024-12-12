from celery import shared_task
import csv
from .models import PriceData
import logging


logger = logging.getLogger('celery')
@shared_task
def process_csv_file(file_path):
    logger.info(f"processing file : {file_path}")
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                PriceData.objects.create(store_id=row['Store ID'],
                    sku=row['SKU'],
                    name=row['Product Name'],
                    price=row['Price'],
                    date=row['Date'])
        logger.info(f"finished processing file {file_path}")
        return True
    except Exception as e:
        logger.error(f'Error processing file {file_path} : {e}')