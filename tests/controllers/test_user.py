import unittest

from app.controllers import user as user_controller
from tests import BaseTestCase
from tests.user import TEST_USER_DATA


class UserTestCase(BaseTestCase):
    @staticmethod
    def create_test_user():
        """Reusable function for testing"""
        user_controller.create_user(**TEST_USER_DATA)

    def test_create_user(self):
        self.create_test_user()
        username = TEST_USER_DATA.get("username")

        # verify user was created in database
        user = user_controller.get_by_username(username)
        self.assertIsNotNone(user)

        self.assertEqual(user.username, username)

        user = user_controller.get_by_username("emperor-fredrik")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
