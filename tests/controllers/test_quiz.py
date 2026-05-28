import unittest

from app.controllers import quiz as quiz_controller
from tests import BaseTestCase


class QuizTestCase(BaseTestCase):
    def test_create_quiz(self):
        created_quiz = quiz_controller.create("janedoe", "Flask Tournament")
        found_quiz = quiz_controller.get_quiz_by_id(created_quiz.id)
        self.assertIsNotNone(found_quiz)

    def test_edit_quiz(self):
        created_quiz = quiz_controller.create("janedoe", "Flask Tournament")
        quiz_controller.update_quiz_by_id(created_quiz.id, dict(title="Flask Arena"))
        updated_quiz = quiz_controller.get_quiz_by_id(created_quiz.id)
        self.assertEqual(updated_quiz.title, "Flask Arena")

    def test_add_questions_to_quiz(self):
        created_quiz = quiz_controller.create("janedoe", "Flask Tournament")
        question1 = dict(description="What is 2 + 2?",
                         correct_answer="4",
                         wrong_answers=["1", "3", "5"])
        question2 = dict(description="What is 1 + 1?",
                         correct_answer="2",
                         wrong_answers=["1", "3", "5"])
        quiz_controller.add_question_to_quiz(question1, created_quiz.id)
        quiz_controller.add_question_to_quiz(question2, created_quiz.id)

        updated_quiz = quiz_controller.get_quiz_by_id(created_quiz.id)
        self.assertIsNotNone(updated_quiz.questions)
        self.assertTrue(len(updated_quiz.questions) == 2)


if __name__ == "__main__":
    unittest.main()
