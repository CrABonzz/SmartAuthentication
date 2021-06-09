from tkinter import StringVar, Label, Button, END

from Utils.common import AUTH_METHODS
from Utils.tkinter_utils import add_screen, destroy_screens, add_entry, info_screen

login_success = True


class Login(object):
    def __init__(self, authenticator, main_screen, photo_grid_screen, text_screen, pixels_screen, lines_screen):
        self.authenticator = authenticator
        self.main_screen = main_screen
        self.photo_grid_screen = photo_grid_screen
        self.pixels_screen = pixels_screen
        self.text_screen = text_screen
        self.lines_screen = lines_screen

        self.login_screen = None
        self.user_not_found_screen = None
        self.login_success_screen = None
        self.username_login_entry = None
        self.email_login_entry = None

        self.username = StringVar()
        self.email = StringVar()

    def login_window(self):
        self.login_screen = add_screen(self.main_screen, "Login", "200x200")

        Label(self.login_screen, text="Please enter your details").pack()

        Label(self.login_screen, text="").pack()

        self.username_login_entry = add_entry(self.login_screen, "Username", self.username)
        self.email_login_entry = add_entry(self.login_screen, "Email", self.email)

        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Start authentication", width=20, height=1, command=self._start_auth).pack()

    def _start_auth(self):
        username = self.username.get()
        email = self.email.get()

        self.username_login_entry.delete(0, END)  # TODO: where?
        self.email_login_entry.delete(0, END)  # TODO: where?

        user_exists, user_blocked = self.authenticator.check_user_exists(username, email, True)
        if not user_exists:
            info_screen(self.login_screen, "User not found", "150x100")
            return

        # If there were many failed entries, the user is blocked
        if user_blocked:
            info_screen(self.login_screen, "User is temporary blocked", "150x100")
            return

        # Get all the authentication ways the user registered to
        auth_methods = self.authenticator.get_authentication_methods(username)

        authentication_classes = {"grid": self.photo_grid_screen,
                                  "pixels": self.pixels_screen,
                                  "text": self.text_screen,
                                  "lines": self.lines_screen}

        # Create and wait for each authentication way
        for auth_method in AUTH_METHODS:
            if auth_method in auth_methods:
                screen = authentication_classes[auth_method]
                screen.handle_login(self.login_screen, username, email)

                self.login_screen.wait_window(screen.screen)

                if not login_success:
                    return

        if login_success:
            self._login_success()

    def _login_success(self):
        self.login_success_screen = add_screen(self.login_screen, "Success", "128x128")

        Label(self.login_success_screen, text="Login Success").pack()
        Button(self.login_success_screen, text="OK",
               command=lambda: destroy_screens(self.login_success_screen, self.login_screen)).pack()
