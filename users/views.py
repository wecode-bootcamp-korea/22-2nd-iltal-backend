import json

from django.views import View
from django.http  import JsonResponse
from users.models import User, Host

class HostView(View):
    def post(self, request, user_id):
        try:
            hostuser    = json.loads(request.body)
            user        = User.objects.get(id = user_id)
            nickname    = hostuser['nickname']
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
            hostuser = Host.objects.select_related('user').get(user_id = user_id)
            result   = {
                'id'            : hostuser.id,
                'user_id'       : hostuser.user_id,
                'nickname'      : hostuser.nickname,
                'profile_url'   : hostuser.profile_url
            }

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        return JsonResponse(result, status=200)       