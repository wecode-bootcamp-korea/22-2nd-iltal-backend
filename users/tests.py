import json
from sys import path
import jwt

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
        Host.objects.create (
            id          = 1,
            nickname    = 'anhesu',
            profile_url = 'testurl',
            user_id     = 1
        )
        self.client.head
    def tearDown(self):
        Host.objects.all().delete() 

    def test_hostview_get_success(self):
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.Rycaz6XldIy-q-xnORvTDQcdfOvEuTrE1BSSf74AiEQ")
        response = client.get('/users/host', content_type='application/json')
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.json(),{"id":1,"user_id":1,"nickname":"anhesu","profile_url":"testurl"})

    def test_hostview_get_Host_Not_Exists(self):
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.VKQ8Cu0rSzuQzmduGTZb1YnF3nB0U7cGqseq1T8RSjs")
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
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.VKQ8Cu0rSzuQzmduGTZb1YnF3nB0U7cGqseq1T8RSjs")
        host = {
            "nickname":"anhesu11",
            "profile_url":"test_url2"
        }
        response = client.post('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,201)
        self.assertEquals(response.json(),{"MESSAGE":"SUCCESS"})

    def test_hostview_post_duple_user(self):
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.Rycaz6XldIy-q-xnORvTDQcdfOvEuTrE1BSSf74AiEQ")
        host = {
            "nickname":"anhesu11",
            "profile_url":"test_url2"
        }
        response = client.post('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,404)
        self.assertEquals(response.json(),{"MESSAGE": "DUPLE_USER"})

    def test_hostview_post_keyerror(self):
        User.objects.create(
            id          = 2,
            kakao_id    = 11,
            name        = 'anhesu11',
            profile_url = 'testurl11',
            email       ='anhesu111@naver.com',
            password    = '12345'
        )
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.VKQ8Cu0rSzuQzmduGTZb1YnF3nB0U7cGqseq1T8RSjs")
        host = {
            "nickname":"anhesu11",
            "profileurl":"test_url2"
        }
        response = client.post('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'KEY_ERROR'})   

    def test_hostview_patch_success(self):
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.Rycaz6XldIy-q-xnORvTDQcdfOvEuTrE1BSSf74AiEQ")
        host = {
            "nickname":"anhesu13",
            "profile_url":"test_url23"
        }
        response = client.patch('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,201)
        self.assertEquals(response.json(),{"MESSAGE":"SUCCESS"})

    def test_hostview_patch_keyerror(self):
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.Rycaz6XldIy-q-xnORvTDQcdfOvEuTrE1BSSf74AiEQ")
        host = {
            "nickname":"anhesu13",
            "profileurl":"test_url23"
        }
        response = client.patch('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'KEY_ERROR'})

    def test_hostview_patch_host_not_exists(self):
        client = Client(HTTP_USER_AGENT="Mozilla/5.0 ...", HTTP_Authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.VKQ8Cu0rSzuQzmduGTZb1YnF3nB0U7cGqseq1T8RSjs")
        host = {
            "nickname":"anhesu13",
            "profileurl":"test_url23"
        }
        response = client.patch('/users/host', json.dumps(host), content_type='application/json')
        self.assertEquals(response.status_code,401)
        self.assertEquals(response.json(),{'message': 'INVALID_USER'})                 