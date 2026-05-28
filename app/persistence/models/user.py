from pymongo.collection import Collection

from .base import Document
from ..db import db


class User(Document):
    collection: Collection = db.users

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
