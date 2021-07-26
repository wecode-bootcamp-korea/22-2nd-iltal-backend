import boto3
import uuid

from django.http     import JsonResponse

from iltal.settings  import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY
from logging         import error

def upload_data(file):

    try :

        s3_client = boto3.client(
                        's3',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                    )
        filename = uuid.uuid4().hex
        s3_client.upload_fileobj(
            file,
            'hsahnprojectdb',
            filename,
            ExtraArgs = {
                "ContentType": file.content_type,
            }
        )
    except error as e:        
        return JsonResponse({"MESSAGE": e}, status=404)

    return 'https://hsahnprojectdb.s3.us-east-2.amazonaws.com/' + filename