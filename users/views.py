import json

from django.views import View
from django.http  import JsonResponse
from users.models import User, Host

class HostView(View):
    def post(self, request, user_id):
        try:
            host    = json.loads(request.body)
            user        = User.objects.get(id = user_id)
            nickname    = host['nickname']
            profile_url = user.profile_url
            is_deleted  = 0
            
            if Host.objects.filter(user_id = user.id) :
                return JsonResponse({"MESSAGE": "DUPLE_USER"}, status=404)

            Host.objects.create(
                user_id     = user.id,
                nickname    = nickname,
                profile_url = profile_url,
                is_deleted  = is_deleted
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    def get(self, request, user_id):
        try:
            host = Host.objects.get(user_id = user_id)
            result   = {
                'id'            : host.id,
                'user_id'       : host.user_id,
                'nickname'      : host.nickname,
                'profile_url'   : host.profile_url
            }

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        return JsonResponse(result, status=200)       