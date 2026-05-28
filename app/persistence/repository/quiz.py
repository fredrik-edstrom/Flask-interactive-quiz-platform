from bson import ObjectId

from app.persistence.models.quiz import Quiz
from app.persistence.models.user import User
from app.persistence.repository import user_repo
from app.shared.resultlist import ResultList


# region Quiz

def create(**kwargs) -> Quiz:
    quiz = Quiz(kwargs)
    quiz.save()
    return quiz


def get_quiz_by_id(_id: str) -> Quiz | None:
    return Quiz(Quiz.collection.find_one(dict(_id=ObjectId(_id))))


def get_all_quizzes() -> list[Quiz] | None:
    return ResultList(Quiz(item) for item in Quiz.collection.find())


def update_quiz_by_id(_id: str, new_data: dict) -> None:
    quiz = get_quiz_by_id(_id)
    quiz.update_with(new_data)


def delete_quiz_by_id(_id: str) -> None:
    quiz = get_quiz_by_id(_id)
    remove_quiz_from_user(quiz.id, quiz.created_by)
    quiz.delete()


def delete_all_quizzes_by(query: dict | None = None) -> int:
    result = Quiz.collection.delete_many(query if query else {})
    return result.deleted_count


def get_all_quizzes_with_title(title: str) -> list[Quiz] | None:
    return [Quiz(data) for data in
            Quiz.collection.find(dict(title={"$regex": title}))]


# endregion Quiz


# region Quiz-Question

def add_question_to_quiz(question_data: dict, quiz_id: str) -> None:
    quiz = get_quiz_by_id(quiz_id)

    if not has_questions(quiz):
        quiz.questions = []

    quiz.questions.append(question_data)
    quiz.save()


def get_question_from_quiz(question_index: int, quiz_id: str) -> dict | None:
    quiz = get_quiz_by_id(quiz_id)
    if not quiz or not has_questions(quiz) or not has_question(question_index, quiz):
        return None

    return quiz.questions[question_index]


def has_updated_question_in_quiz(question_index: int, quiz_id: str, new_data: dict) -> bool:
    quiz = get_quiz_by_id(quiz_id)

    if not quiz or not has_questions(quiz) or not has_question(question_index, quiz):
        return False

    edit_question_in_quiz(question_index, quiz, new_data)
    return True


def edit_question_in_quiz(question_index: int, quiz: Quiz, new_data: dict) -> None:
    quiz.questions = [question if index != question_index else new_data
                      for index, question in enumerate(quiz.questions)]
    quiz.save()


def has_removed_question_from_quiz(question_index: int, quiz_id: str) -> bool:
    quiz = get_quiz_by_id(quiz_id)

    if not quiz or not has_questions(quiz) or not has_question(question_index, quiz):
        return False

    remove_question_from_quiz(question_index, quiz)
    return True


def remove_question_from_quiz(question_index: int, quiz: Quiz) -> None:
    quiz.questions = [question for index, question in enumerate(quiz.questions)
                      if index != question_index]

    if quiz.questions == []:
        del quiz.questions

    quiz.save()


def remove_all_questions_in_quiz(quiz_id: str) -> None:
    quiz = get_quiz_by_id(quiz_id)
    if not quiz or not has_questions(quiz):
        return

    del quiz.questions
    quiz.save()


def has_question(question_index: int, quiz: Quiz) -> bool:
    return quiz.questions is not None and question_index < len(quiz.questions)


def has_questions(quiz: Quiz) -> bool:
    return hasattr(quiz, "questions")


def is_questions_empty(questions: list) -> bool:
    return questions == []


# endregion Quiz-Question


# region Quiz-User


def get_all_quizzes_by_username(username: str) -> list[Quiz] | None:
    return ResultList(Quiz(item) for item in Quiz.collection.find(dict(created_by=username)))


def delete_all_quizzes_by_username(username: str) -> int:
    quizzes = get_all_quizzes_by_username(username)

    if not quizzes:
        return 0

    for quiz in quizzes:
        remove_quiz_from_user(quiz.id, username)

    return delete_all_quizzes_by(dict(created_by=username))


def has_quiz(quiz_id: str, user: User) -> bool:
    return quiz_id in user.quizzes


def has_quizzes(user: User) -> bool:
    return hasattr(user, "quizzes")


def add_quiz_to_user(quiz_id: str, username: str) -> None:
    user = user_repo.get_by_username(username)

    if not user:
        return None

    if not has_quizzes(user):
        user.quizzes = []

    if has_quiz(quiz_id, user):
        return

    user.quizzes.append(quiz_id)
    user.save()


def remove_quiz_from_user(quiz_id: str, username: str) -> None:
    user = user_repo.get_by_username(username)
    if not user or not has_quizzes(user) or not has_quiz(quiz_id, user):
        return

    for index, _id in enumerate(user.quizzes):
        if _id == quiz_id:
            user.quizzes.pop(index)

            if not user.quizzes:
                del user.quizzes

            user.save()

# endregion Quiz-User
