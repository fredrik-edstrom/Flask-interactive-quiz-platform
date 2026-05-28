from os import getenv

from pymongo import MongoClient
from pymongo.database import Database

from app import ConfigType

PROTOCOL = getenv("MONGO_DB_PROTOCOL")
USER = getenv("MONGO_DB_USER")
PASS = getenv("MONGO_DB_PASS")
HOST = getenv("MONGO_DB_HOST")
PORT = getenv("MONGO_DB_PORT")
DB_NAME = getenv("MONGO_DB_NAME")

MONGO_DB_URL = getenv("MONGO_DB_URL")
ENV = getenv("PROJECT_ENV")

config = ConfigType(ENV.lower())

if config != ConfigType.PRODUCTION:
    MONGO_DB_URL = f"{PROTOCOL}://{USER}:{PASS}@{HOST}:{PORT}"
    DB_NAME += "-dev" if config == ConfigType.DEVELOPMENT else "-test"

client: MongoClient = MongoClient(MONGO_DB_URL, authSource="admin")
db: Database = client[DB_NAME]


def init_mongodb(uri: str, name: str) -> None:
    global client, db

    client = MongoClient(uri, authSource="admin")
    db = client[name]


def drop_database(name: str) -> None:
    client.drop_database(name)
