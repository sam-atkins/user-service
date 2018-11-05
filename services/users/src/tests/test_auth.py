import json
import time

from flask import current_app

from src.tests.base import BaseTestCase
from src.tests.utils import add_user
from src.tests.datasets import users


class TestAuthBlueprint(BaseTestCase):
    """Auth route tests"""

    def test_user_registration(self,):
        with self.client:
            response = self.client.post(
                'auth/register',
                data=json.dumps({
                    'username': 'sam',
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplication_email(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response = self.client.post(
                'auth/register',
                data=json.dumps({
                    'username': 'sam',
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_duplication_username(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'sam',
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That user already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'sam',
                    'password': 'weakpassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'sam',
                    'email': 'sam@example.com',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        with self.client:
            add_user(
                users.USER_ONE.get('username'), users.USER_ONE.get('email'),
                users.USER_ONE.get('password'))
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json',
            )
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout', headers={'Authorization': f'Bearer {token}'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout', headers={'Authorization': 'Bearer invalid'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        with self.client:
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'sam@example.com',
                    'password': 'weakpassword'
                }),
                content_type='application/json')
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status', headers={'Authorization': f'Bearer {token}'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'sam')
            self.assertTrue(data['data']['email'] == 'sam@example.com')
            self.assertTrue(data['data']['active'] is True)
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status', headers={'Authorization': 'Bearer invalid'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)
