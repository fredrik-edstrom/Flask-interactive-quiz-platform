from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, InputRequired, Email, EqualTo, DataRequired


class SignupForm(FlaskForm):

    email = StringField('E-mail: ', validators=[DataRequired(message='Please enter a valid Email!!'),
                                                Email(message='Please enter a valid Email')])

    username = StringField('Username: ', validators=[DataRequired(message='This is required'), Length(3, 25)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(3, 30)])
    repeat_pass = PasswordField('Repeat Password:', validators=[DataRequired(), EqualTo('password')])

    create_user = SubmitField('Sign up!')


class LoginForm(FlaskForm):

    username = StringField('Username: ', validators=[InputRequired()])
    password = PasswordField('Password: ', validators=[InputRequired()])

    login_button = SubmitField('Login')


class ForgotPasswordForm(FlaskForm):

    email = StringField('E-mail: ', validators=[DataRequired(message='Please enter a valid Email!!'),
                                                Email(message='Please enter a valid Email')])

    request_button = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):

    new_password = PasswordField('New Password: ', validators=[InputRequired(), Length(3, 25)])
    repeat_password = PasswordField('Repeat New Password: ', validators=[InputRequired(),
                                                                         EqualTo('new_password',
                                                                                 message='Password must match')])
    reset_button = SubmitField('Reset Password')


class UpdateForm(FlaskForm):

    password = PasswordField('Current Password: ', validators=[InputRequired()])
    new_password = PasswordField('New Password: ', validators=[InputRequired(), Length(3, 25)])
    repeat_password = PasswordField('Repeat New Password: ', validators=[InputRequired(),
                                                                         EqualTo('new_password',
                                                                                 message='Password must match')])
    first_name = StringField('Name: ')
    country = StringField('Country: ')

    update_button = SubmitField('Update')


class RandomAvatarForm(FlaskForm):
    random_button = SubmitField('Randomize')


class ResendVerificationForm(FlaskForm):
    resend_button = SubmitField('Resend')
