import unittest

from src.api.models import User
from src import db
from src.tests.base import BaseTestCase
from src.tests.utils import add_user
from src.tests.datasets import users


class TestUserModel(BaseTestCase):
    """Tests for the User Model."""

    def test_to_json(self):
        user = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_add_user(self):
        user = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'sam')
        self.assertEqual(user.email, 'sam@example.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_passwords_are_random(self):
        user_one = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        user_two = add_user(
            users.USER_TWO.get('username'), users.USER_TWO.get('email'),
            users.USER_TWO.get('password'))
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'),
            users.USER_ONE.get('password'))
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)


if __name__ == 'main':
    unittest.main()
