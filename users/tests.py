from sys import path
import json, bcrypt, jwt, requests

from django.http                import JsonResponse, cookie
from django.http.response       import HttpResponse
from django.views.generic.base  import View
from django.http                import request, response
from django.test                import TestCase, Client, client, utils
from django.test                import RequestFactory

from unittest.mock              import patch, MagicMock
from users.models               import Host, User
from my_settings                import SECRET_KEY,ALGORITHM

class SignupViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            email       = "wlgns432@gmail.com",
            password    = "1234asdf!",
            name        = "dmwkdm"
        )
    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_post_success(self):
        client = Client()
        user = {
            'email'     : 'wldkwmd122@gmail.com',
            'password'  : 'a123aaaa!',
            'name'      : 'dmwkdm'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                "MESSAGE" : "SUCCESS"
            }
        )

    def test_signupview_post_invalid_email(self):
        client = Client()
        user = {
            'email'     : 'wwwwwwgmail.com',
            'password'  : 'a123aaaa!',
            'name'      : 'dmwkdm'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "MESSAGE" : "INVALID EMAIL"
            }
        )

    def test_signupview_post_invalid_password(self):
        client = Client()
        user = {
            'email'     : 'wwwwww@gmail.com',
            'password'  : 'a123aaaa',
            'name'      : 'dmwkdm' 
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "MESSAGE" : "INVALID PASSWORD"
            }
        )

    def test_signupview_post_duplicated_email(self):
        client = Client()
        user = {
            'email'       : "wlgns432@gmail.com",
            'password'    : "1234asdf!",
            'name'        : "dmwkdm"
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "MESSAGE" : "EXIST EMAIL"
            }
        )

    def test_signupview_post_invalid_keys(self):
        client = Client()
        user = {
            'ddemail'    : 'wlgns432@gmail.com',
            'password'   : '1234asdf!',
            'name'       : 'dmwkdm',
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "KEY_ERROR"
            }
        )

class SigninViewTest(TestCase):
    def setUp(self):
        password    = 'wlaa1234!'

        User.objects.create(
            id          = 1,
            password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            email       = 'BrendanEich@gmail.com',
            name        = 'gimgimgim'
        )

        access_token= jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
         User.objects.all().delete()

    # token 검증
    def test_signinview_post_success(self):

        client = Client()
        user = {
            'email'    : 'BrendanEich@gmail.com',
            'password' : 'wlaa1234!'
        }

        response       = client.post('/users/signin', json.dumps(user), content_type="application/json")
        access_token   = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message'       : 'success',
                'access_token'  : access_token
            }
        )

    # keyerror
    def test_signinview_post_keyerror(self):

        client = Client()

        user = {
            'password' : 'wlaa1234!'
        }

        response = client.post('/users/signin', json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                "message" : "KEY_ERROR"
            }
        )

    # password error
    def test_signinview_post_not_password(self):

        client = Client()

        user = {
            'password'  : 'wlaa1232!',
            'email'     : 'BrendanEich@gmail.com',
        }

        response = client.post('/users/signin', json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                "message" : "INVALID_USER"
            }
        )

    # email error
    def test_signinview_post_does_not_existed_email(self):

        client = Client()

        user = {
            'password'  : 'wlaa1234!',
            'email'     : 'Brendah@gmail.com',
        }

        response = client.post('/users/signin', json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                "message" : "INVALID_USER"
            }
        )

class HostTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            kakao_id    = 1,
            name        = 'anhesu',
            profile_url = 'testurl',
            email       ='anhesu1@naver.com',
            password    = '1234'
        )
        self.client.head
    
    def test_hostview_get_success(self):
        Host.objects.create (
            id          = 1,
            nickname    = 'anhesu',
            profile_url = 'testurl',
            user_id     = 1
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM))
        response = client.get('/users/host', content_type='application/json')
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.json(),{"id":1,"user_id":1,"nickname":"anhesu","profile_url":"testurl"})

    def test_hostview_get_Host_Not_Exists(self):
        Host.objects.create (
            id          = 1,
            nickname    = 'anhesu',
            profile_url = 'testurl',
            user_id     = 1
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 2}, SECRET_KEY, ALGORITHM))
        response = client.get('/users/host', content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'INVALID_USER'})
    
    def test_hostview_post_success(self):
        User.objects.create(
            id          = 2,
            kakao_id    = 11,
            name        = 'anhesu11',
            profile_url = 'testurl11',
            email       ='anhesu111@naver.com',
            password    = '12345'
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM))
        host = {
            "nickname":"anhesu11",
            "profile_url":"test_url2"
        }
        response = client.post('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,201)
        self.assertEquals(response.json(),{"MESSAGE":"SUCCESS"})

    def test_hostview_post_duple_user(self):
        Host.objects.create (
            id          = 1,
            nickname    = 'anhesu',
            profile_url = 'testurl',
            user_id     = 1
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM))
        host = {
            "nickname":"anhesu11",
            "profile_url":"test_url2"
        }
        response = client.post('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,404)
        self.assertEquals(response.json(),{"MESSAGE": "DUPLE_USER"})

    def test_hostview_post_keyerror(self):
        
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 2}, SECRET_KEY, ALGORITHM))
        host = {
            "nicknamee":"anhesu11",
            "profileurl":"test_url2"
        }
        response = client.post('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'KEY_ERROR'})   

    def test_hostview_patch_success(self):
        Host.objects.create (
            id          = 1,
            nickname    = 'anhesu',
            profile_url = 'testurl',
            user_id     = 1
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM))
        host = {
            "nickname":"anhesu13",
            "profile_url":"test_url23"
        }
        response = client.patch('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,201)
        self.assertEquals(response.json(),{"MESSAGE":"SUCCESS"})

    def test_hostview_patch_keyerror(self):
        Host.objects.create (
            id          = 1,
            nickname    = 'anhesu',
            profile_url = 'testurl',
            user_id     = 1
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM))
        host = {
            "nicknamee":"anhesu13",
            "profileurl":"test_url23"
        }
        response = client.patch('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'KEY_ERROR'})

    def test_hostview_patch_host_not_exists(self):
        
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = jwt.encode({"user_id": 2}, SECRET_KEY, ALGORITHM))
        host = {
            "nickname":"anhesu13",
            "profileurl":"test_url23"
        }
        response = client.patch('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'HOST_ERROR'})           
