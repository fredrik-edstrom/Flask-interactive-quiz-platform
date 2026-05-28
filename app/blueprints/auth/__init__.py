from flask import Blueprint

bp_auth = Blueprint(name="auth",
                    import_name=__name__,
                    template_folder="templates",
                    static_folder="static")

from app.blueprints.auth import views
