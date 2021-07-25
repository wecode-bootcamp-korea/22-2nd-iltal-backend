import json

from django.http    import response
from django.test    import TestCase, Client

from unittest.mock  import patch, MagicMock
from users.models   import Host, User

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
            profile_url = 'testurl'
        )
        User.objects.create(
            id          = 2,
            kakao_id    = 1,
            name        = 'anhesu',
            profile_url = 'testurl'
        )
        Host.objects.create (
            nickname    = "test",
            user_id     = 1,
            profile_url = 'testurl'
        )

    def test_hostview_post_success(self):
        client = Client()
        host   = {
            'nickname'   : 'anhesu',
            'profile_url': 'testurl',
            'user_id'    : 2
        }
        response = client.post('/users/host/2',json.dumps(host),content_type='application/json')
        self.assertEqual(response.status_code,201)

    def test_hostview_post_keyerror(self):
        client = Client()
        host   = {
            'nickname'   : 'anhesu',
            'profileurl': 'testurl',
            'userid'    : 2
        }
        response = client.post('/users/host/2',json.dumps(host),content_type='application/json')
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{"MESSAGE":"KEY_ERROR"})

    def test_hostview_post_user_notexists(self):
        client = Client()
        host   = {
            'nicknamee'   : 'anhesu',
            'profileurll': 'testurl',
            'useridd'    : 20
        }
        response = client.post('/users/host/2',json.dumps(host),content_type='application/json')
        self.assertEqual(response.status_code,404)

    def test_hostview_get(self):
        client   = Client()
        response = client.get('/users/host/1',content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{'id': 1, 'user_id': 1, 'nickname': 'test', 'profile_url': 'testurl'})

    def test_hostview_get_host_notexists(self):
        client   = Client()
        response = client.get('/users/host/10',content_type='application/json')
        self.assertEqual(response.status_code,404)

    def test_hostview_patch_success(self):
        client = Client()
        host   = {
            'nickname'   : 'modifynickname',
            'profile_url': 'modifyurl'
        }
        response = client.patch('/users/host/1',json.dumps(host),content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),{"MESSAGE":"SUCCESS"})

    def test_hostview_patch_keyerror(self):
        client = Client()
        host   = {
            'nicknamee'   : 'modifynickname',
            'profileurll': 'modifyurl'
        }
        response = client.patch('/users/host/1',json.dumps(host),content_type='application/json')
        self.assertEqual(response.status_code,404)

    def test_hostview_post_host_notexists(self):
        client = Client()
        host   = {
            'nickname'   : 'modifynickname',
            'profileurl': 'modifyurl'
        }
        response = client.patch('/users/host/1',json.dumps(host),content_type='application/json')
        self.assertEqual(response.status_code,404)