import io
import os
import re
import boto3
import json
import uuid

from django.views    import View
from django.http     import JsonResponse

from datetime        import datetime
from products.models import Product
from iltal.settings  import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

class ProductView(View):
    def post(self, request):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )

            background_url = request.FILES["background_url"]
            filename = uuid.uuid4().hex
            s3_client.upload_fileobj(
                background_url,
                'hsahnprojectdb',
                filename,
                ExtraArgs = {
                    "ContentType": background_url.content_type,
                }
            )
            Product.objects.create (
                title           =  request.POST.get('title'),
                region          =  request.POST.get('region'),
                coordinate      =  [{"test":"aa"}],
                price           =  request.POST.get('price'),
                is_group        =  request.POST.get('is_group'),
                background_url  =  'https://hsahnprojectdb.s3.us-east-2.amazonaws.com/' + filename,
                is_deleted      =  False,
                host_id         =  request.POST.get('host_id'),
                subcategory_id  =  request.POST.get('subcategory_id')
            )    

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)    