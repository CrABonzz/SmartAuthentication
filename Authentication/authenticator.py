import binascii
import hashlib
import json

import math

from Utils.common import HASH_ITERATIONS_AMOUNT, HASH_RESULT_SIZE, DISTANCE_GRANUALITY


class Authenticator(object):
    def __init__(self):
        self.users = None
        self.update_users_file()

    def update_users_file(self):
        with open(r"assets\users.json", 'r') as users_file:
            all_users = json.load(users_file)
            self.users = all_users["users"]

    def check_user_exists(self, username, email):
        user = [user for user in self.users if user['user'] == username and user['email'] == email]
        return len(user), user[0]["blocked"]

    def get_authentication_methods(self, username):
        passwords = next(user["passwords"] for user in self.users if user['user'] == username)

        optional = [key for key in passwords.keys() if passwords[key] != ""]
        return ["text"] + optional

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

    def verify_pixels_password(self, username, clicks):
        password = next(user["passwords"]["pixels"] for user in self.users if user['user'] == username)
        coordinates = [(int(coor.split("-")[0]), int(coor.split("-")[1])) for coor in password.split(", ")[:-1]]

        if len(coordinates) != len(clicks):
            return False

        return all(self._click_close(click, expected_click) for click, expected_click in zip(clicks, coordinates))

    def _click_close(self, click, expected_click):
        dist = math.hypot(expected_click[0] - click[0], expected_click[1] - click[1])
        return dist < DISTANCE_GRANUALITY
