from app.persistence.repository import quiz as quiz_repo
from app.shared import schemas


# region Quiz

def create(created_by: str,
           title: str,
           ) -> schemas.Quiz:
    data = dict(created_by=created_by, title=title)

    quiz: quiz_repo.Quiz = quiz_repo.create(**data)
    add_quiz_to_user(quiz.id, created_by)
    return schemas.Quiz(**quiz.to_dict())


def get_quiz_by_id(quiz_id: str) -> schemas.Quiz | None:
    quiz: quiz_repo.Quiz = quiz_repo.get_quiz_by_id(quiz_id)
    return schemas.Quiz(**quiz.to_dict()) if quiz else None


def get_all_quizzes() -> list[schemas.Quiz] | None:
    quizzes: list[quiz_repo.Quiz] = quiz_repo.get_all_quizzes()
    return [schemas.Quiz(**quiz.to_dict()) for quiz in quizzes] if quizzes else None


def update_quiz_by_id(quiz_id: str, new_data: dict) -> None:
    quiz_repo.update_quiz_by_id(quiz_id, new_data)


def delete_quiz_by_id(quiz_id: str) -> None:
    quiz_repo.delete_quiz_by_id(quiz_id)


def delete_all_quizzes_by(query: dict | None = None) -> int:
    return quiz_repo.delete_all_quizzes_by(query)


def get_all_quizzes_with_title(title: str) -> list[schemas.Quiz] | None:
    quizzes: list[quiz_repo.Quiz] = quiz_repo.get_all_quizzes_with_title(title)
    return [schemas.Quiz(**quiz.to_dict()) for quiz in quizzes] if quizzes else None


# endregion Quiz


# region Quiz-Question

def add_question_to_quiz(question_data: dict, quiz_id: str) -> None:
    quiz_repo.add_question_to_quiz(question_data, quiz_id)


def get_question_from_quiz(question_index: int, quiz_id: str) -> schemas.Question | None:
    question_data = quiz_repo.get_question_from_quiz(question_index, quiz_id)
    return schemas.Question(**question_data) if question_data else None


def has_updated_question_in_quiz(question_index: int, quiz_id: str, new_data: dict) -> bool:
    return quiz_repo.has_updated_question_in_quiz(question_index, quiz_id, new_data)


def has_removed_question_from_quiz(question_index: int, quiz_id: str) -> bool:
    return quiz_repo.has_removed_question_from_quiz(question_index, quiz_id)


def remove_all_questions_in_quiz(quiz_id: str) -> None:
    quiz_repo.remove_all_questions_in_quiz(quiz_id)


# endregion Quiz-Question


# region Quiz-User


def get_all_quizzes_by_username(username: str) -> list[schemas.Quiz] | None:
    quizzes: list[quiz_repo.Quiz] = quiz_repo.get_all_quizzes_by_username(username)
    return [schemas.Quiz(**quiz.to_dict()) for quiz in quizzes]


def delete_all_quizzes_by_username(username: str) -> int:
    return quiz_repo.delete_all_quizzes_by_username(username)


def add_quiz_to_user(quiz_id: str, username: str) -> None:
    return quiz_repo.add_quiz_to_user(quiz_id, username)


def remove_quiz_from_user(quiz_id: str, username: str) -> None:
    return quiz_repo.remove_quiz_from_user(quiz_id, username)

# endregion Quiz-User
