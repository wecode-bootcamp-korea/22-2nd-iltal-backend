import json, re, bcrypt, jwt
import users.utils
import core.views

from django.views       import View
from django.http        import JsonResponse
from django.shortcuts   import get_object_or_404

from users.models       import User, Host
from my_settings    import SECRET_KEY, ALGORITHM

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
class SigninView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({"message":"success","access_token": access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

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
            
            if Host.objects.filter(user_id = request.user.id).exists() :
                return JsonResponse({"MESSAGE": "DUPLE_USER"}, status=404)

            Host.objects.create(
                user_id     = request.user.id,
                nickname    = request.POST.get('nickname'),
                profile_url = core.views.upload_data(request.FILES["background_url"])
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
            host             = get_object_or_404(Host, user_id = request.user.id)
            host.nickname    =request.POST.get('nickname')
            host.profile_url = core.views.upload_data(request.FILES["background_url"])
            host.save()

        except AttributeError :
            return JsonResponse({'message': 'INVALID_USER'}, status=401) 

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

        except Host.DoesNotExist:
            return JsonResponse({'message': 'HOST_ERROR'}, status=401) 
                        
        return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)   

