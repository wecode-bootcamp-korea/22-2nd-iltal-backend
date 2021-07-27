from django.views    import View
from django.http     import JsonResponse

from products.models import Product
from my_settings     import BUCKET, SECRET_KEY, ALGORITHM
from iltal.settings  import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY
from core.views      import AWSAPI

class ProductView(View):
    def post(self, request):
        try:
            aws = AWSAPI(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET)

            Product.objects.create (
                title           =  request.POST.get('title'),
                region          =  request.POST.get('region'),
                price           =  request.POST.get('price'),
                is_group        =  request.POST.get('is_group'),
                background_url  =  aws.upload_file(request.FILES.get('background_url')),
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