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
            data = json.loads(request.body)
            Product.objects.create (
                title           =  data['title'],
                region          =  data['region'],
                price           =  data['price'],
                is_group        =  data['is_group'],
                background_url  =  core.views.upload_data(data['background_url']),
                is_deleted      =  False,
                host_id         =  data['host_id'],
                subcategory_id  =  data['subcategory_id']
            )    

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)    