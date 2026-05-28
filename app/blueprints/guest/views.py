from flask import render_template
from app.persistence.repository.game import get_score_by_username

from . import bp_guest


@bp_guest.get("/home")
@bp_guest.get("/")
def index():
    return render_template("guest/index.html")


@bp_guest.get("/about")
def about():
    return render_template("guest/about.html")


@bp_guest.get("/leaderboard")
def leaderboard():
    return render_template("guest/leaderboard.html")
