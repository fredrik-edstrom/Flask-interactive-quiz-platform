from flask import render_template, request, jsonify, make_response
from flask_login import login_required, current_user

from .. import bp_user




@bp_user.route('/test')
@login_required
def hello_world():
    return render_template('user/chat.html', username=current_user.username)


@bp_user.route("/play")
def play():
    return render_template("user/../../game/play.html", data=dummyQuiz[current_question])


@bp_user.route("/play/next", methods=["POST"])
def update_question():
    correct_answer = 2
    request_ = request.get_json()
    print(request_)

    response_ = make_response(jsonify(correct_answer))

    return response_
