import json, re, bcrypt

from django.views       import View
from django.http        import JsonResponse
from django.shortcuts   import get_object_or_404

from users.models       import User, Host
import users.utils

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

        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"}, status = 400)

        return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)

class HostView(View):
    @users.utils.user_validator
    def get(self, request):
        try:
            host = Host.objects.get(user_id = request.user.id)
            result   = {
                'id'            : host.id,
                'user_id'       : host.user_id,
                'nickname'      : host.nickname,
                'profile_url'   : host.profile_url
            }
        except AttributeError :
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

        except Host.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        return JsonResponse(result, status=200) 
    
    @users.utils.user_validator      
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id = request.user.id)
            if Host.objects.filter(user_id = user.id).exists() :
                return JsonResponse({"MESSAGE": "DUPLE_USER"}, status=404)
            Host.objects.create(
                user_id     = user.id,
                nickname    = data['nickname'],
                profile_url = data['profile_url'],
                is_deleted  = False
            )

        except AttributeError :
            return JsonResponse({'message': 'INVALID_USER'}, status=401)   

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401) 

        return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)
    
    @users.utils.user_validator    
    def patch(self, request):
            try:
                data             = json.loads(request.body)
                host             = get_object_or_404(Host,user_id = request.user.id)
                host.nickname    = data['nickname']
                host.profile_url = data['profile_url']
                host.save()

            except AttributeError :
                return JsonResponse({'message': 'INVALID_USER'}, status=401) 

            except KeyError:
                return JsonResponse({'message': 'KEY_ERROR'}, status=401)

            except Host.DoesNotExist:
                return JsonResponse({'message': 'HOST_ERROR'}, status=401) 
                           
            return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)   