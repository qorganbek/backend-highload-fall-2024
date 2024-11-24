import csv
from celery import shared_task
from .models import FileUpload

@shared_task
def process_file(file_upload_id):
    upload = FileUpload.objects.get(id=file_upload_id)
    upload.status = 'Processing'
    upload.save()

    try:
        with open(upload.file.path, 'r') as f:
            reader = csv.reader(f)
            # some staff happens here with the csv. Creating own s3 is pretty hard
        upload.status = 'Completed'
    except Exception as e:
        upload.status = 'Failed'
        print(f"Error: {e}")
    finally:
        upload.save()