class Authenticate(object):
    def __init__(self):
        with open(r"assets\users.txt") as users_file:
            self.users = users_file.readlines()

    def check_user_exists(self, username):
        return username == "user"

    def verify_user(self, username, password):
        return username + " " + password in self.users
