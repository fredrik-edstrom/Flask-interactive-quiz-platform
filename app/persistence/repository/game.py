from bson import ObjectId

from . import quiz as quiz_repo
from app.persistence.models.game import Game
from ...shared.resultlist import ResultList
from ...shared.schemas import Player


def create(**kwargs) -> Game:
    game = Game(kwargs)
    game.save()
    return game


def get_game_by_id(_id: str) -> Game | None:
    try:
        return Game(Game.collection.find_one(dict(_id=ObjectId(_id))))
    except TypeError:
        return None


def answer_question_on_game_and_get_correct_answer(game_id: str, answer: str) -> str:
    game = get_game_by_id(game_id)
    quiz = quiz_repo.get_quiz_by_id(game.quiz_id)
    index = game.__dict__["player"]["on_question_index"]
    correct_answer = quiz.questions[index]["correct_answer"]
    new_data = game.__dict__

    if answer == correct_answer:
        new_data["player"]["score"] = game.__dict__["player"]["score"] + 1

    if index + 1 < len(quiz.questions):
        new_data["player"]["on_question_index"] = \
            game.__dict__["player"]["on_question_index"] + 1

    if not index + 1 < len(quiz.questions):
        new_data["player"]["has_finished"] = True

    game.update_with(new_data)
    game.save()

    return correct_answer


def get_all_games():
    return ResultList(Game(item) for item in Game.collection.find())


def get_score_by_username(username: str) -> list:

        games = get_all_games()
        results = []
        for game in games:
            if game.__dict__["player"]["username"] == username \
                    and game.__dict__["player"]["has_finished"]:
                results.append(game.__dict__)
        return results