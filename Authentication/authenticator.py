import json
import math
import re

from Utils.common import HASH_RESULT_SIZE, DISTANCE_GRANUALITY, DIGIT_REGEX, SYMBOL_REGEX, \
    LOWERCASE_REGEX, UPPERCASE_REGEX
from Utils.password_utils import hash_password


class Authenticator(object):
    def __init__(self):
        self.users = None
        self.update_users_file()

    def update_users_file(self):
        """
        Get the dump of the users from the file
        :return:
        """
        with open(r"assets\users.json", 'r') as users_file:
            all_users = json.load(users_file)
            self.users = all_users["users"]

    def check_user_exists(self, username, email, check_blocked=False):
        """
        Check there is a signed user with this credentials
        :return: If the user exists, and if blocked
        """
        user = [user for user in self.users if user['user'] == username and user['email'] == email]
        if 0 != len(user) and check_blocked:
            return len(user), user[0]["blocked"]
        return len(user), None

    def get_photos_ids(self, username, email):
        """
        Get the user photos used in the grid authentications way.
        Every user get random 9 photos.
        """
        user = [user for user in self.users if user['user'] == username and user['email'] == email][0]
        return user["grid_photos_ids"]

    def get_authentication_methods(self, username):
        """
        Get all kinds of authentication ways the user registered
        """
        passwords = next(user["passwords"] for user in self.users if user['user'] == username)

        return [key for key in passwords.keys() if passwords[key] != ""]

    def _verify_generic_password(self, username, password_input, password_type):
        password = next(user["passwords"][password_type] for user in self.users if user['user'] == username)
        salt, hashed_password = password[:HASH_RESULT_SIZE], password[HASH_RESULT_SIZE:]

        return hashed_password == hash_password(password_input, salt.encode('ascii'), False)

    def verify_user_text_password(self, username, password_input):
        return self._verify_generic_password(username, password_input, "text")

    def verify_user_grid_password(self, username, password_input):
        return self._verify_generic_password(username, password_input, "grid")

    def verify_pixels_password(self, username, clicks):
        password = next(user["passwords"]["pixels"] for user in self.users if user['user'] == username)

        coordinates = [coor[:-2] for coor in password]
        coordinates = [(int(coor.split("-")[0]), int(coor.split("-")[1])) for coor in coordinates]

        if len(coordinates) != len(clicks):
            return False

        return all(self._click_close(click, expected_click) for click, expected_click in zip(clicks, coordinates))

    def verify_lines_password(self, username, password_input):
        return self._verify_generic_password(username, password_input, "lines")

    def _click_close(self, click, expected_click):
        """
        Determine if the 2 coordinates are close or not
        :param click: The click the user clicked
        :type click: tuple<int, int>
        :param expected_click: The click stored as password
        :type expected_click: tuple<int, int>
        :return: True if the clicks are close enough
        :rtype: bool
        """
        dist = math.hypot(expected_click[0] - click[0], expected_click[1] - click[1])
        return dist < DISTANCE_GRANUALITY

    def password_strong(self, password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            6 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        error_messages = [error_message for regex, error_message in
                          [DIGIT_REGEX, UPPERCASE_REGEX, LOWERCASE_REGEX, SYMBOL_REGEX] if re.search(regex,
                                                                                                     password) is None]

        password_error_message = "\n".join(error_messages)
        if len(password) < 6:
            password_error_message += "\nPassword length should be above 6.\n"

        return password_error_message
