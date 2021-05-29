from tkinter import StringVar, Label, Entry, Button, END

from Screens.AuthenticationScreens.grid_photos_screen import GridPhotosScreen
from Screens.AuthenticationScreens.pixels_screen import PixelsScreen
from Screens.AuthenticationScreens.text_screen import TextScreen
from Utils.tkinter_utils import add_screen, destroy_screens, add_entry, info_screen

login_success = True


class Login(object):
    def __init__(self, authenticator, main_screen):
        self.main_screen = main_screen
        self.login_screen = None

        self.authenticator = authenticator

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

        user_exists, user_blocked = self.authenticator.check_user_exists(username, email)
        if not user_exists:
            info_screen(self.login_screen, "User not found", "150x100")
            return

        if user_blocked:
            info_screen(self.login_screen, "User is temporary blocked", "150x100")
            return

        auth_methods = self.authenticator.get_authentication_methods(username)

        authentication_classes = {"grid": GridPhotosScreen, "pixels": PixelsScreen, "text": TextScreen}

        for auth_method in ["text", "grid", "pixels"]:  # TODO: move to const
            if auth_method in auth_methods:
                screen = authentication_classes[auth_method](self)
                screen.create(username, email)

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
