import io
import os
import boto3
import json
from io  import BytesIO
from django.core import files
from django.views    import View
from django.http     import JsonResponse
from django.core.files.images import ImageFile

from datetime import datetime
from products.models import Product
from iltal.settings  import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

class ProductView(View):
    def post(self, request):
        try:
            #data = json.loads(request.body)

            # if Product.objects.filter(host_id = data['host_id']).exists() :
            #     return JsonResponse({"MESSAGE": "PRODUCT_EXISTS"}, status=404)

            s3_client = boto3.client(
                's3',
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )
            
            background_url = request.FILES["background_url"]
            s3_client.upload_fileobj(
                background_url,
                'hsahnprojectdb',
                'test',
                ExtraArgs = {
                    "ContentType": background_url.content_type,
                }
            )
            # image_url = "http://dkinterest.s3.ap-northeast-2.amazonaws.com/"+image_time+"."+image_type
            # image_url = image_url.replace(" ","/")
            #Pin.objects.create(image_url = image_url)

            # Product.objects.create(
            #     title           =  data["title"],
            #     region          =  data["region"],
            #     price           =  data["price"],
            #     is_group        =  data["is_group"],
            #     background_url  =  data["background_url"],
            #     is_deleted      =  False,
            #     host_id         =  data["host_id"],
            #     subcategory_id  =  data["subcategory_id"]
            # )    

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)    