from flask import render_template
from flask_login import login_required

from .. import bp_user


@bp_user.get("/search")
@login_required
def search():
    return render_template("user/search.html")
