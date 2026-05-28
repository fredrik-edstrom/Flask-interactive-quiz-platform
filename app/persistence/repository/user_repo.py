import hashlib

from werkzeug.security import generate_password_hash, check_password_hash

from app.persistence.models.user import User
from app.shared.resultlist import ResultList


def create_user(email: str, username: str, password: str) -> [list]:
    """Creates a user in database, if validation from Check_existing_users passes"""

    data = dict(
        email=email,
        username=username,
        password=password,
        is_admin=False,
        is_active=True,
        is_confirmed=False,
        is_confirmed_since=None,
        avatar=f"https://robohash.org/{get_email_hash(email)}/set_set4/3.14159?size=400x500")

    if check_existing_users(username, email):
        user = User(data)
        user.save()
        return user


def get_email_hash(email):
    return hashlib.blake2s(email.encode()).hexdigest()


def get_all_users():
    return ResultList(User(i) for i in User.collection.find())


def get_by_username(username: str):
    return ResultList(User(i) for i in User.collection.find(dict(username=username))).first_or_none()


def get_by_email(email: str):
    return ResultList(User(i) for i in User.collection.find(dict(email=email))).first_or_none()


def update_by_username(username, new_data):
    user = get_by_username(username)
    user.update_with(new_data)


def check_existing_users(username: str, email: str) -> bool:
    """ Returns True if Email or username doesn't exist in the database"""

    if User.collection.find_one({"username": username}) is not None:
        print(f"{username} already exists in database")
        return False

    if User.collection.find_one({"email": email}) is not None:
        print(f"{email} already exists in database")
        return False
    return True


def get_all_usernames_with(search_for: str) -> list[str] | None:
    return [User(data).username for data in
            User.collection.find(dict(username={"$regex": search_for}))]
