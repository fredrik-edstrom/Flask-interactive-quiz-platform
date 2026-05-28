from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from .. import bp_user
from ..forms.question import CreateQuestionForm, EditQuestionForm
from ..utils import get_clean_question_form_data
from app.controllers import quiz as quiz_controller


@bp_user.get("/quizzes/<quiz_id>/questions")
@login_required
def create_question_get(quiz_id: str):
    if not quiz_controller.get_quiz_by_id(quiz_id):
        flash("Quiz not found.", category="error")
        return redirect(url_for(".view_profile"))

    return render_template("user/question/create.html",
                           form=CreateQuestionForm(),
                           quiz_id=quiz_id)


@bp_user.post("/quizzes/<quiz_id>/questions")
@login_required
def create_question_post(quiz_id: str):
    if not quiz_controller.get_quiz_by_id(quiz_id):
        flash("Quiz not found.", category="error")
        return redirect(url_for(".view_profile"))

    form = CreateQuestionForm()
    if form.validate_on_submit():
        clean_data = get_clean_question_form_data(form.data)
        quiz_controller.add_question_to_quiz(clean_data, quiz_id)

        flash("Question created successfully.", category="success")
        return redirect(url_for(".detail_quiz_get",
                                quiz_id=quiz_id))

    flash("Failed to create question.", category="error")
    return render_template("user/question/create.html",
                           form=form)


@bp_user.get("/quizzes/<quiz_id>/questions/<int:question_index>")
@login_required
def detail_question_get(quiz_id: str, question_index: int):
    question = quiz_controller.get_question_from_quiz(question_index, quiz_id)

    if not question:
        flash("Question not found.", category="error")
        return redirect(url_for(".view_profile"))

    return render_template("user/question/detail.html",
                           question=question)


@bp_user.get("/quizzes/<quiz_id>/questions/<int:question_index>/edit")
@login_required
def edit_question_in_quiz_get(quiz_id: str, question_index: int):
    question = quiz_controller.get_question_from_quiz(question_index, quiz_id)

    if not question:
        flash("Question not found.", category="error")
        return redirect(url_for(".view_profile"))

    form = EditQuestionForm(obj=question)
    return render_template("user/question/edit.html",
                           form=form,
                           quiz_id=quiz_id,
                           question_index=question_index)


@bp_user.post("/quizzes/<quiz_id>/questions/<int:question_index>/edit")
@login_required
def edit_question_in_quiz_post(quiz_id: str, question_index: int):
    form = EditQuestionForm()
    if form.validate_on_submit():
        new_data = get_clean_question_form_data(form.data)

        if not quiz_controller.has_updated_question_in_quiz(question_index, quiz_id, new_data):
            flash("Something went wrong when attempting to update a Question.", category="success")
        else:
            flash("Question edited successfully.", category="success")
        return redirect(url_for(".detail_quiz_get",
                                quiz_id=quiz_id))
    else:
        return render_template("user/question/edit.html",
                               form=form,
                               question_index=question_index,
                               quiz_id=quiz_id)


@bp_user.get("/quizzes/<quiz_id>/questions/<int:question_index>/delete")
@login_required
def delete_question_in_quiz(quiz_id: str, question_index: int):
    if not quiz_controller.has_removed_question_from_quiz(question_index, quiz_id):
        flash("Something went wrong when attempting to delete a Question.", category="error")
    else:
        flash("Question deleted successfully.", category="success")
    return redirect(url_for(".detail_quiz_get",
                            quiz_id=quiz_id))


@bp_user.get("/quizzes/<quiz_id>/questions/delete")
@login_required
def delete_all_questions_in_quiz(quiz_id: str):
    if not quiz_controller.get_quiz_by_id(quiz_id):
        flash("Quiz not found.", category="error")
    else:
        quiz_controller.remove_all_questions_in_quiz(quiz_id)
        flash("Quiz questions deleted successfully.", category="success")
    return redirect(url_for(".detail_quiz_get",
                            quiz_id=quiz_id))
