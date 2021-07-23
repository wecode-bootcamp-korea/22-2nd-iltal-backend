import json, re, bcrypt

from django.views import View
from django.http  import JsonResponse
from users.models import User, Host
from users.models import User

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