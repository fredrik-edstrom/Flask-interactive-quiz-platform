from flask import Blueprint

bp_api = Blueprint(name="api",
                   import_name=__name__,
                   template_folder="templates",
                   static_folder="static")

from . import endpoints
