from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired


class BaseQuizForm(FlaskForm):
    title = wtf.StringField("Title", validators=[DataRequired()])


class CreateQuizForm(BaseQuizForm):
    submit = wtf.SubmitField("Create Quiz")


class EditQuizForm(BaseQuizForm):
    submit = wtf.SubmitField("Edit Quiz")
