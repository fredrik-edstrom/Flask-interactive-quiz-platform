from flask import Blueprint

bp_guest = Blueprint(name="guest",
                     import_name=__name__,
                     template_folder="templates",
                     static_folder="static")

from . import views


