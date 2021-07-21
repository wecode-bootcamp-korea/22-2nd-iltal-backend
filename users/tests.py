import json

from django.test import TestCase, Client

from users.models import User

class SignupViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            email       = "wlgns432@gmail.com",
            password    = "1234asdf!",
            name        = "dmwkdm"
        )

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

    def tearDown(self):
        User.objects.all().delete()