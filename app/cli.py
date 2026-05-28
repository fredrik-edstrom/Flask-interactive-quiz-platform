from flask import Flask


def register_cli_commands(_app: Flask) -> None:
    @_app.cli.command()
    def test():
        """Runs all the unit tests of this project.

        Open a terminal and navigate to this project's root
        directory and type 'flask test' to run all tests.
        """

        import unittest
        tests = unittest.TestLoader().discover("tests")
        unittest.TextTestRunner(verbosity=2).run(tests)
