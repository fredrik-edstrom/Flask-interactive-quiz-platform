from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired, ValidationError


def unique_questions_required(form, field):
    correct_answer = field.data
    wrong_answers = form.wrong_answers.data

    choices = [answer.lower() for answer in ([correct_answer] + wrong_answers)]
    answers_set = set(choices)

    if len(answers_set) != len(choices):
        raise ValidationError("All answers must be unique. No duplicates allowed.")


class BaseQuestionForm(FlaskForm):
    description = wtf.StringField("Description", validators=[
        DataRequired("A question requires a description.")])
    correct_answer = wtf.StringField("Correct Answer", validators=[
        DataRequired(message="A question requires a correct answer."),
        unique_questions_required])
    wrong_answers = wtf.FieldList(wtf.StringField(validators=[
        DataRequired("A wrong answer is required.")]),
        min_entries=3, max_entries=3)


class CreateQuestionForm(BaseQuestionForm):
    submit = wtf.SubmitField("Create Question")


class EditQuestionForm(BaseQuestionForm):
    submit = wtf.SubmitField("Edit Question")
