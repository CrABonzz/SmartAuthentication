import binascii
import hashlib
import json

from Utils.common import HASH_ITERATIONS_AMOUNT, HASH_RESULT_SIZE


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

    def get_authentication_methods(self, username):
        passwords = next(user["passwords"] for user in self.users if user['user'] == username)
        return [key for key in passwords.keys() if passwords[key] != ""]

    def verify_password(self, username, password_input, password_type):
        password = next(user["passwords"][password_type] for user in self.users if user['user'] == username)
        salt, hashed_password = password[:HASH_RESULT_SIZE], password[HASH_RESULT_SIZE:]

        hashed_password_input = hashlib.pbkdf2_hmac(
            'sha512',
            password_input.encode('utf-8'),
            salt.encode('ascii'),
            HASH_ITERATIONS_AMOUNT
        )

        return hashed_password == binascii.hexlify(hashed_password_input).decode('ascii')

    def verify_user_text_password(self, username, password_input):
        return self.verify_password(username, password_input, "text")

    def verify_user_grid_password(self, username, password_input):
        return self.verify_password(username, password_input, "grid")
