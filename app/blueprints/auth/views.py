from http import HTTPStatus
from os import urandom
from random import randrange

from flask import render_template, flash, redirect, url_for, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

import app
from . import bp_auth
from .forms import SignupForm, LoginForm, UpdateForm, ForgotPasswordForm, ResetPasswordForm, RandomAvatarForm, \
    ResendVerificationForm
from ...controllers import user as user_controller
from ...controllers.user import get_by_username
from app.services import security_service

from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import datetime


@bp_auth.route("/signup/", methods=['GET', 'POST'])
def signup():
    username = None
    form = SignupForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    # If all fields in form is correct...
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        token = serializer.dumps(email)

        if user_controller.check_existing_users(username, email):

            user_controller.create_user(email, username, password)

            msg = Message('Confirmed E-mail Address', sender=current_app.config["MAIL_SENDER"], recipients=[email])
            link = url_for('auth.confirm_email', token=token, _external=True)
            msg.body = 'To verify your E-mail address, visit the following link: {}'.format(link)
            app.mail.send(msg)

            return render_template("auth/email_verification_sent.html")
        else:
            flash('Username Already Exists')

    return render_template("auth/signup.html", username=username, form=form)


@bp_auth.route('/confirm/<token>')
def confirm_email(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(token, max_age=3600)
    except:
        return render_template("auth/invalid_token.html")

    user = user_controller.get_by_email(email)

    if user.is_confirmed:
        flash('Account already confirmed')
    else:
        user.is_confirmed = True
        user.is_confirmed_since = datetime.datetime.now()
        user.save()

        return render_template('auth/verified.html')

    return render_template('guest/index.html')


@bp_auth.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = user_controller.get_by_username(username)

        if user is not None:
            if user_controller.is_password_valid(user, password):
                if user.is_confirmed:
                    login_user(user)
                    flash(user.email)
                    flash(user.username)

                    return redirect(url_for("user.view_profile", username=user.username))

                else:

                    return redirect(url_for("auth.not_verified", username=user.username))
            else:
                flash('Invalid Credentials')

        else:
            flash('Invalid Credentials')

    return render_template("auth/login.html", form=form)


@bp_auth.route("/not_verified/<username>", methods=['GET', 'POST'])
def not_verified(username):

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    user = user_controller.get_by_username(username)

    form = ResendVerificationForm()

    if not user:
        abort(HTTPStatus.NOT_FOUND, "This is not the account you want to verify.")

    if user.is_confirmed:
        flash("Account already verified")
        redirect(url_for("guest.index"))

    if form.validate_on_submit():

        token = serializer.dumps(user.email)

        msg = Message('Confirmed E-mail Address', sender=current_app.config["MAIL_SENDER"], recipients=[user.email])
        link = url_for('auth.confirm_email', token=token, _external=True)
        msg.body = 'To verify your E-mail address, visit the following link: {}'.format(link)
        app.mail.send(msg)

        return render_template("auth/email_verification_sent.html")

    return render_template("auth/not_verified.html", form=form)


@bp_auth.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('guest.index'))


@bp_auth.route("/forgot_password/", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        flash("You're already logged in... If you would like to change password go to edit profile page.")
        return redirect(url_for('guest.index'))

    form = ForgotPasswordForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    if form.validate_on_submit():
        email = form.email.data
        user_email = user_controller.get_by_email(email)

        token = serializer.dumps(email)

        if user_email is not None and user_email.is_confirmed:

            msg = Message('Password Reset Request', sender=current_app.config["MAIL_SENDER"], recipients=[email])
            link = url_for('auth.reset_password', token=token, _external=True)
            msg.body = 'To reset your password, visit the following link: {}'.format(link)
            app.mail.send(msg)

            return render_template("auth/password_request_sent.html")

        else:
            flash("Email is not in use")

    return render_template("auth/forgot_password.html", form=form)


@bp_auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash("You're already logged in... If you would like to change password go to edit profile page.")
        return redirect(url_for('guest.index'))

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(token, max_age=3600)
    except:
        return render_template('auth/invalid_token.html')

    user = user_controller.get_by_email(email)
    form = ResetPasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        user_controller.update_by_username(
            user.username,
            new_data={"password": security_service.generate_password_hash(new_password)}
        )
        flash("Password Updated Successfully!")
        return redirect(url_for('guest.index'))
    return render_template('auth/reset_password.html', form=form)


@bp_auth.route('/update/<string:username>', methods=['GET', 'POST'])
@login_required
def update(username):
    form = UpdateForm()
    rform = RandomAvatarForm()
    new_password = form.new_password.data
    password = form.password.data

    user = get_by_username(username)

    if form.update_button.data and form.validate():

        if user_controller.is_password_valid(user, password):

            user_controller.update_by_username(current_user.username, new_data={"password": security_service.
                                               generate_password_hash(new_password)})
            user_controller.update_by_username(current_user.username, new_data={"first_name": form.first_name.data})
            user_controller.update_by_username(current_user.username, new_data={"country": form.country.data})

            flash('User Updated Successfully!')

            return redirect(url_for('guest.index'))

        else:
            flash('Invalid Credentials')

    if rform.random_button.data and rform.validate():
        random_avatar = urandom(8).hex()
        random_figure = (randrange(4)+1)
        user_controller.update_by_username(current_user.username, new_data={"avatar": f"https://robohash.org/"
                                                        f"{random_avatar}/set_set{random_figure}/3.14159?size=400x500"})
        return render_template("auth/update.html", usernmane=username, form=form, rform=rform,
                               random_avatar=random_avatar, random_figure=random_figure)

    return render_template("auth/update.html", username=username, form=form, rform=rform)

