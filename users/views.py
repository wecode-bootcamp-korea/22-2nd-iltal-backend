import json, re, bcrypt

from django.http      import JsonResponse
from django.views     import View

from users.models import User, Host

class SignupView(View):
    def post(self, request):

        data = json.loads(request.body)
        EMAIL_REGES    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        PASSWORD_REGES = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,16}$'

        try:

            if not re.search(EMAIL_REGES, data["email"]):
                return JsonResponse ({"MESSAGE":"INVALID EMAIL"}, status = 400)

            if not re.search(PASSWORD_REGES, data["password"]):
                return JsonResponse ({"MESSAGE": "INVALID PASSWORD"}, status = 400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse ({"MESSAGE":"EXIST EMAIL"}, status = 400)

            hashed_passwored = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email           = data["email"],
                password        = hashed_passwored,
                name            = data["name"],
            )

            return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"}, status = 400)

class HostView(View):
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

        except Host.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_HOST"}, status=404)
        
        return JsonResponse(result, status=200)       
    def post(self, request, user_id):
        try:
            data        = json.loads(request.body)
            user        = User.objects.get(id = user_id)            
            if Host.objects.filter(user_id = user.id).exists() :
                return JsonResponse({"MESSAGE": "DUPLE_USER"}, status=404)

            Host.objects.create(
                user_id     = user.id,
                nickname    = data['nickname'],
                profile_url = data['profile_url'],
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
                host             = Host.objects.get(user_id = user_id)
                host.nickname    = data['nickname']
                host.profile_url = data['profile_url']
                host.save()

            except KeyError:
                return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)

            except Host.DoesNotExist:
                return JsonResponse({"MESSAGE": "INVALID_HOST"}, status=404)
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)