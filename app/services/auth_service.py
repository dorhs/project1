import hashlib
from app.vers import *
from app.models import handlers


def verify_password(username, password, users):
    for user in users:
        if user["username"] == username:
            if user['password'] == hashlib.md5(password.encode()).hexdigest():
                return True, "Login successful"
    return False, "Wrong Authentication"


def update_password(username, password, users, path):
    try:
        newusers = []
        for user in users:
            if username == user['username']:
                user["password"] = hashlib.md5(password.encode()).hexdigest()
            newusers.append(user)
        handlers.dumpJson(path, newusers)
        logger.info(f"Update the password for the user {username}")
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False


def register_user(username, password):
    _, users = handlers.checkFile(f"{outputDir}/{usersjsonfile}")
    for user in users:
        if user["username"] == username:
            return False, "Can't create this username"
    users.append({"username": username, "password": hashlib.md5(password.encode()).hexdigest(), "image": "static/images/avater.jpg"})
    status = handlers.dumpJson(f"{outputDir}/{usersjsonfile}", users)
    if status:
        return True, "Registration successful"
    else:
        return False, "Registration Error"


def login_user(username, password):
    _, users = handlers.loadJson(f"{outputDir}/{usersjsonfile}")
    if username == "" or password == "":
        return False, "Can't use empty values"
    status, msg = verify_password(username, password, users)
    return status, msg


def replace_password(username, password, new_password):
    path = f"{outputDir}/{usersjsonfile}"
    _, users = handlers.loadJson(path)
    if username == "" or password == "" or new_password == "":
        return False, "Can't use empty values", "danger"
    status, msg = verify_password(username, password, users)
    if status:
        status = update_password(username, new_password, users, path)
        if status:
            return True, "Your password has been updated successfully!", "success"
        return False, "The current password is incorrect.", "danger"
    return False, "Can't change the password, try again!", "danger"
