from pymongo.collection import Collection

from .base import Document
from ..db import db


class Quiz(Document):
    collection: Collection = db.quizzes
