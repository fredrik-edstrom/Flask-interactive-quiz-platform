from pymongo.collection import Collection

from .base import Document
from ..db import db


class Game(Document):
    collection: Collection = db.games

