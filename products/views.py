import json
import uuid
import core.views 

from django.views    import View
from django.http     import JsonResponse

from datetime        import datetime
from products.models import Product

class ProductView(View):
    def post(self, request):
        try:
            print(request.FILES.get('background_url'))
            Product.objects.create (
                title           =  request.POST.get('title'),
                region          =  request.POST.get('region'),
                price           =  request.POST.get('price'),
                is_group        =  request.POST.get('is_group'),
                background_url  =  core.views.upload_data(request.FILES.get('background_url')),
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