from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import bp_user
from ..forms.quiz import CreateQuizForm, EditQuizForm
from app.controllers import quiz as quiz_controller


@bp_user.get("/quizzes")
@login_required
def create_quiz_get():
    return render_template("user/quiz/create.html", form=CreateQuizForm())


@bp_user.post("/quizzes")
@login_required
def create_quiz_post():
    form = CreateQuizForm()

    if form.validate_on_submit():
        quiz = quiz_controller.create(created_by=current_user.username, title=form.title.data)

        flash("Quiz created successfully.", category="success")
        return redirect(url_for(".detail_quiz_get", quiz_id=quiz.id))

    flash("Failed to create quiz.", category="error")
    return render_template("user/quiz/create.html", form=form)


@bp_user.get("/quizzes/<quiz_id>")
@login_required
def detail_quiz_get(quiz_id: str):
    quiz = quiz_controller.get_quiz_by_id(quiz_id)

    if not quiz:
        flash("Question not found.", category="error")
        return redirect(url_for(".view_profile"))

    return render_template("user/quiz/detail.html", quiz=quiz)


@bp_user.get("/quizzes/<quiz_id>/edit")
@login_required
def edit_quiz_get(quiz_id: str):
    quiz = quiz_controller.get_quiz_by_id(quiz_id)
    form = EditQuizForm(obj=quiz)

    return render_template("user/quiz/edit.html", form=form)


@bp_user.post("/quizzes/<quiz_id>/edit")
@login_required
def edit_quiz_post(quiz_id: str):
    form = EditQuizForm()

    if form.validate_on_submit():

        if not quiz_controller.get_quiz_by_id(quiz_id):
            flash("Quiz not found.", category="error")

        else:
            quiz_controller.update_quiz_by_id(quiz_id, new_data=dict(title=form.title.data))

            flash("Quiz updated successfully.", category="success")
            return redirect(url_for(".view_profile", username=current_user.username))

    flash("Failed to update quiz.", category="error")
    return render_template("user/quiz/edit.html", form=form)


# TODO: only owner or admin should be able to delete
@bp_user.get("/quizzes/<quiz_id>/delete")
@login_required
def delete_quiz(quiz_id: str):
    if not quiz_controller.get_quiz_by_id(quiz_id):
        flash("Quiz not found.", category="error")
    else:
        quiz_controller.delete_quiz_by_id(quiz_id)

        flash("Quiz deleted successfully.", category="success")
    return redirect(url_for(".view_profile", username=current_user.username))


@bp_user.get("/quizzes/delete")
@login_required
def delete_my_quizzes():
    deleted_quizzes = quiz_controller.delete_all_quizzes_by_username(current_user.username)

    flash(f"{deleted_quizzes} quizzes deleted from your account.", category="success")
    return redirect(url_for(".view_profile"))
