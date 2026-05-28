from enum import Enum
from os import environ, urandom
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Config:
    SECRET_KEY = environ.get("SECRET_KEY") or urandom(32).hex()

    # MongoDB
    MONGO_DB_NAME = environ.get("MONGO_DB_NAME") or "pyhoot-mongo-db"
    MONGO_DB_PROTOCOL = environ.get("MONGO_DB_PROTOCOL")
    MONGO_DB_USER = environ.get("MONGO_DB_USER")
    MONGO_DB_PASS = environ.get("MONGO_DB_PASS")
    MONGO_DB_HOST = environ.get("MONGO_DB_HOST")
    MONGO_DB_PORT = environ.get("MONGO_DB_PORT")
    MONGO_DB_URL = environ.get("MONGO_DB_URL")

    # Flask-Mail
    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = environ.get("MAIL_USE_TLS")
    MAIL_SENDER = environ.get("MAIL_SENDER")
    MAIL_PORT = environ.get("MAIL_PORT")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    CSRF_ENABLED = False


__configs = {
    ConfigType.DEVELOPMENT: DevelopmentConfig,
    ConfigType.PRODUCTION: ProductionConfig,
    ConfigType.TESTING: TestingConfig,
}


def configure(_app: Flask, config_type: ConfigType) -> None:
    from .persistence.db import init_mongodb

    _app.config.from_object(__configs[config_type])

    if config_type != ConfigType.PRODUCTION:
        _app.config["MONGO_DB_URL"] = (f"{_app.config['MONGO_DB_PROTOCOL']}://{_app.config['MONGO_DB_USER']}:"
                                       f"{_app.config['MONGO_DB_PASS']}@{_app.config['MONGO_DB_HOST']}:"
                                       f"{_app.config['MONGO_DB_PORT']}")

    db_name = _app.config["MONGO_DB_NAME"]

    if config_type == ConfigType.DEVELOPMENT:
        db_name += "-dev"
    elif config_type == ConfigType.TESTING:
        db_name += "-test"

    _app.config["MONGO_DB_NAME"] = db_name

    init_mongodb(_app.config["MONGO_DB_URL"], _app.config["MONGO_DB_NAME"])
