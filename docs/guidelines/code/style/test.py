import unittest

from tests import BaseTestCase


class SomeTestCase(BaseTestCase):
    def setUp(self) -> None:
        """Is run once before each test."""
        super().setUp()

        # additional setup logic
        pass

    def tearDown(self) -> None:
        """Is run once after each test."""
        super().tearDown()

        # additional tear down logic
        pass

    @classmethod
    def setUpClass(cls) -> None:
        """Is run once before all tests."""
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        """Is run once after all tests."""
        pass


if __name__ == "__main__":
    unittest.main()
