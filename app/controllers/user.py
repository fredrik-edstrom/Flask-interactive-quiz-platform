from app import login_manager

from app.persistence.models.user import User
from app.persistence.repository import user_repo as repo
from app.services import security_service


def create_user(email: str, username: str, password: str):
    password = security_service.generate_password_hash(password)
    return repo.create_user(email, username, password)


def get_email_hash(email):
    return repo.get_email_hash(email)


def get_by_username(username: str):
    return repo.get_by_username(username)


def get_by_email(email: str):
    return repo.get_by_email(email)


def check_existing_users(username: str, email: str):
    return repo.check_existing_users(username, email)


def is_password_valid(user: User, plain_password: str) -> bool:
    return security_service.is_password_valid(plain_password, user.password)


def get_all_users():
    return repo.get_all_users()


def update_by_username(username, new_data):
    return repo.update_by_username(username, new_data)


def get_all_usernames_with(search_for: str) -> list[str] | None:
    return repo.get_all_usernames_with(search_for)


@login_manager.user_loader
def load_user(user_id: str) -> User:
    return get_by_username(user_id)
