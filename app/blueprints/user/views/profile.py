from http import HTTPStatus

from flask import abort, render_template
from flask_login import login_required

from .. import bp_user
from app.controllers import quiz as quiz_controller
from app.controllers import user as user_controller


@bp_user.get("/profile/<username>")
def view_profile(username: str):
    if not user_controller.get_by_username(username):
        abort(HTTPStatus.NOT_FOUND, "This is not the profile you are looking for.")
    quizzes = quiz_controller.get_all_quizzes_by_username(username)
    return render_template("user/profile/view.html",
                           quizzes=quizzes, username=username)

