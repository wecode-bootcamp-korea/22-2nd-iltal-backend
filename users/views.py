import json

from django.views import View
from django.http  import JsonResponse

from users.models import User, Host

class HostView(View):

    def get(self, request, user_id):
        try:
            hostuser = Host.objects.get(user_id = user_id)
            result   = {
                'id'            : hostuser.id,
                'user_id'       : hostuser.user_id,
                'nickname'      : hostuser.nickname,
                'profile_url'   : hostuser.profile_url
            }

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except Host.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_HOST"}, status=404)
        
        return JsonResponse(result, status=200)       

    def post(self, request, user_id):
        try:
            data        = json.loads(request.body)
            print(user_id)
            user        = User.objects.get(id = user_id)
            print(user)
            nickname    = data['nickname']
            profile_url = data['profile_url']
            
            if Host.objects.filter(user_id = user.id).exists() :
                return JsonResponse({"MESSAGE": "DUPLE_USER"}, status=404)

            Host.objects.create(
                user_id     = user.id,
                nickname    = nickname,
                profile_url = profile_url,
                is_deleted  = False
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=404)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    def patch(self, request, user_id):
            try:
                data             = json.loads(request.body)
                nickname         = data['nickname']
                profile_url      = data['profile_url']
                host             = Host.objects.get(user_id = user_id)
                host.nickname    = nickname
                host.profile_url = profile_url
                host.save()

            except KeyError:
                return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

            except Host.DoesNotExist:
                return JsonResponse({"MESSAGE": "INVALID_HOST"}, status=404)
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)