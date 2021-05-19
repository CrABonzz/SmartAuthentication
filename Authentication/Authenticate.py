import json


class Authenticate(object):
    def __init__(self):
        self.users = None
        self.update_users_file()

    def update_users_file(self):
        with open(r"assets\users.json", 'r') as users_file:
            all_users = json.load(users_file)
            self.users = all_users["users"]

    def check_user_exists(self, username):
        return any(True for user in self.users if user['user'] == username)

    def verify_user_text_password(self, username, password):
        return next(user["passwords"]["text"] for user in self.users if user['user'] == username) == password
