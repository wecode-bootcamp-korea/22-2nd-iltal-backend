import boto3
import uuid
import logging
from botocore.signers import generate_presigned_url

from django.http     import JsonResponse

class AWSAPI:
    def __init__(self, aws_access_key, aws_secret_key, bucket):
        self.bucket = bucket
        self.storage_url = 'https://' + bucket + '.s3.us-east-2.amazonaws.com/'
        self.client = boto3.client(
            's3',
            aws_access_key_id = aws_access_key,
            aws_secret_access_key = aws_secret_key
        )

    def upload_file(self, file):
        try :
            filename = uuid.uuid4().hex
            self.client.upload_fileobj(
                file,
                self.bucket,
                filename,
                ExtraArgs = {
                    "ContentType": file.content_type,
                }
            )

        except Exception as e:
            logging.error(f"message : {e}")

            return JsonResponse({"MESSAGE": "FAIL_TO_UPLOAD"}, status=404)

        return self.storage_url + filename