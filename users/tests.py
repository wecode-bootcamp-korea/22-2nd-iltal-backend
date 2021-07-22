import json
from django.http import response

from django.test import TestCase, Client

from unittest.mock import patch, MagicMock
from users.models import Host, User

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
