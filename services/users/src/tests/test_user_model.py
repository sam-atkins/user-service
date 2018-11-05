import unittest

from src import db
from src.tests.base import BaseTestCase
from src.tests.utils import add_user
from src.tests.datasets import users


class TestUserModel(BaseTestCase):
    """Tests for the User Model."""

    def test_to_json(self):
        user = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'))
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_add_user(self):
        user = add_user(
            users.USER_ONE.get('username'), users.USER_ONE.get('email'))
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'sam')
        self.assertEqual(user.email, 'sam@example.com')
        self.assertTrue(user.active)


if __name__ == 'main':
    unittest.main()
