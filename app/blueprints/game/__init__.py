from flask import Blueprint

bp_game = Blueprint(name="game",
                    import_name=__name__,
                    template_folder="templates",
                    static_folder="static")

from . import views
