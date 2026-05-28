import json
from http import HTTPStatus

from flask import jsonify, request, render_template
from flask_login import current_user, login_required

from . import bp_game
from app.controllers import game as game_controller

"""
Create a new game:
http://127.0.0.1:5000/game/start/<quiz_id>

Get current game state:
http://127.0.0.1:5000/game/current/<game_id>

Answer question on Game: (send 'user_input' as request param)
http://127.0.0.1:5000/game/answer/<game_id>

Get next question or end results:
http://127.0.0.1:5000/game/next/<game_id>


Testing
-------
Quiz with questions
http://127.0.0.1:5000/game/start/61ef6a6a012d030345364cf1

Quiz without questions
http://127.0.0.1:5000/game/start/61f386951b784fb585d0bb78

"""


# TODO: need to update all routes with JSON web tokens eventually
#       for security and session management.
@bp_game.get("/start/<quiz_id>")
@login_required
def start_game(quiz_id: str):
    game = game_controller.create(current_user.username, quiz_id)

    if not game:
        # TODO: flash (quiz must have at least one question)
        # TODO: redirect to profile

        return jsonify(dict(
            error="Failed to create a Game.",
            message="Quiz must have at least one question.")), HTTPStatus.BAD_REQUEST

    # TODO:
    return render_template("game/play.html", game=game.current_game_state_to_dict())


@bp_game.post("/current/<game_id>")
def get_current_game_state(game_id: str):
    game = game_controller.get_game_by_id(game_id)
    if not game:
        return jsonify(dict(
            error="This is not the game you are looking for.",
            message="There is no game by that id.")), HTTPStatus.NOT_FOUND

    return jsonify(game.current_game_state_to_dict()), HTTPStatus.OK


@bp_game.post("/answer/<game_id>")
def receive_and_process_answer_post(game_id: str):
    """Takes in an answer for further processing and returns the correct answer."""
    game = game_controller.get_game_by_id(game_id)
    if not game:
        return jsonify(dict(
            error="This is not the game you are looking for.",
            message="There is no game by that id.")), HTTPStatus.NOT_FOUND

    if game.player.has_finished:
        data = dict(message="Game is over",
                    has_finished=game.player.has_finished)
        return jsonify(data), HTTPStatus.OK

    user_input = request.json["value"]

    correct_answer = game_controller.answer_question_on_game_and_get_correct_answer(game_id, user_input)
    data = dict(correct_answer=correct_answer,
                has_finished=game.player.has_finished)
    return jsonify(data), HTTPStatus.OK


@bp_game.post("/next/<game_id>")
def get_next_question_or_end_results_post(game_id: str):
    """Returns the next question in the quiz or the end results.

    The client-side can differentiate by checking the key 'has_finished'.
    """
    game = game_controller.get_game_by_id(game_id)
    if not game:
        return jsonify(dict(
            error="This is not the game you are looking for.",
            message="There is no game by that id.")), HTTPStatus.NOT_FOUND

    if game.has_another_question():
        return jsonify(game.current_game_state_to_dict()), HTTPStatus.OK
    return jsonify(game.end_game_results_to_dict()), HTTPStatus.OK
