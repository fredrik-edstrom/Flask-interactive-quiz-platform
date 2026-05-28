from http import HTTPStatus
import unittest

from app.controllers import user as user_controller
from tests import BaseClientTestCase
from tests.user import TEST_USER_DATA


class AuthViewsTestCase(BaseClientTestCase):
    @staticmethod
    def create_test_user():
        user_controller.create_user(**TEST_USER_DATA)

    def login_user_and_return_response(self):
        return self.client.post("/login/", data=dict(
            username=TEST_USER_DATA.get("username"),
            password=TEST_USER_DATA.get("password"),
        ), follow_redirects=True)

    def test_signup_and_login(self):
        # create user
        self.create_test_user()
        user = user_controller.get_by_username(TEST_USER_DATA.get("username"))
        self.assertIsNotNone(user)

        # User is not verified
        self.assertFalse(user.is_confirmed)

        # TODO: redirect to "confirm your email page"

        # User is now confirmed
        user.is_confirmed = True
        user.save()
        self.assertTrue(user.is_confirmed)

        # redirect to login page
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.login_user_and_return_response()
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_fail(self):
        response = self.login_user_and_return_response()
        self.assertTrue("Don't have an account?" in response.get_data(as_text=True))

    def test_change_email(self):
        pass

    def test_change_password(self):
        pass

    def test_forgot_password(self):
        pass

    def test_logout(self):
        self.create_test_user()
        response = self.login_user_and_return_response()
        self.assertEqual(response.status_code, HTTPStatus.OK)

        user = user_controller.get_by_username(TEST_USER_DATA.get("username"))
        self.assertTrue(user.is_authenticated)

        response = self.client.get("/logout")
        self.assertTrue("Unauthorized" in response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
