from http import HTTPStatus

from flask import jsonify, request

from . import bp_api
from app.controllers import quiz as quiz_controller
from app.controllers import user as user_controller


@bp_api.post("/users")
def search_for_usernames():
    username = request.form.get("username")
    usernames = user_controller.get_all_usernames_with(username)
    return jsonify(usernames), HTTPStatus.OK if usernames else HTTPStatus.NOT_FOUND


@bp_api.post("/quizzes")
def search_for_quizzes():
    title = request.form.get("title")
    quizzes = quiz_controller.get_all_quizzes_with_title(title)
    return jsonify(quizzes), HTTPStatus.OK if quizzes else HTTPStatus.NOT_FOUND
