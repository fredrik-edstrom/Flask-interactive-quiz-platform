from flask import Blueprint

bp_user = Blueprint(name="user",
                    import_name=__name__,
                    template_folder="templates",
                    static_folder="static")

from . import views
from app import events
