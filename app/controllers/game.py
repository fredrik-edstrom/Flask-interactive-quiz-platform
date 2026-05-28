from app.controllers import quiz as quiz_controller
from app.controllers import user as user_controller
from app.persistence.repository import game as game_repo
from app.shared import schemas


def create(username: str,
           quiz_id: str,
           ) -> schemas.Game | None:
    if not user_controller.get_by_username(username):
        raise ValueError(f"Could not find a user with the username: {username}.")

    quiz: schemas.Quiz = quiz_controller.get_quiz_by_id(quiz_id)

    if not quiz:
        raise ValueError(f"Could not find a quiz with the id: {quiz_id}.")

    if not quiz.questions:
        return None

    player_data = dict(username=username, score=0,
                       on_question_index=0, has_finished=False)
    game_data = dict(quiz_id=quiz_id, player=player_data)
    game_model: game_repo.Game = game_repo.create(**game_data)

    player = schemas.Player(**player_data)
    game = schemas.Game(game_model.id, player, quiz)

    return game


def get_game_by_id(game_id: str) -> schemas.Game | None:
    game_model: game_repo.Game = game_repo.get_game_by_id(game_id)

    if not game_model:
        return None

    player = schemas.Player(**game_model.player)
    quiz: schemas.Quiz = quiz_controller.get_quiz_by_id(game_model.quiz_id)

    return schemas.Game(game_model.id, player, quiz)


def answer_question_on_game_and_get_correct_answer(game_id: str,
                                                   answer: str
                                                   ) -> str:
    """Updates the game document in the database layer and returns the correct answer.

    Will update the user's score if the answer was correct and increment the user's
    question index if there is a next question, otherwise it sets has_finished to True.
    """
    return game_repo.answer_question_on_game_and_get_correct_answer(game_id, answer)


def get_score_by_username(username):
    return game_repo.get_score_by_username(username)
