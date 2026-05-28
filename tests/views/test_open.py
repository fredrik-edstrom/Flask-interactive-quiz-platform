from http import HTTPStatus
import unittest

from app.controllers import user as user_controller
from tests import BaseClientTestCase
from tests.user import TEST_USER_DATA


class OpenViewsTestCase(BaseClientTestCase):
    def test_guest_visits_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_visits_about(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_visits_signup(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, HTTPStatus.PERMANENT_REDIRECT)

        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_visits_login(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, HTTPStatus.PERMANENT_REDIRECT)

        response = self.client.get("/login/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_visits_profile(self):
        user_controller.create_user(**TEST_USER_DATA)
        response = self.client.get("/profile/janedoe")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_visits_profile_not_found(self):
        response = self.client.get("/profile/jamesbond")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_guest_visits_login_required_page_should_fail(self):
        response = self.client.get("/quizzes")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertTrue("Unauthorized" in response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
