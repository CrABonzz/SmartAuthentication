from tkinter import StringVar, Toplevel, Label, Entry, Button, END, RAISED

from Screens.AuthenticationScreens.grid_photos_screen import GridPhotosScreen
from Screens.AuthenticationScreens.pixels_screen import PixelsScreen
from Screens.AuthenticationScreens.text_screen import TextScreen

login_success = True

class Login(object):
    def __init__(self, authenticator, main_screen):
        self.main_screen = main_screen
        self.login_screen = None

        self.authenticator = authenticator

        self.user_not_found_screen = None
        self.login_success_screen = None
        self.username_login_entry = None

        self.username = StringVar()

    def login_window(self):
        self.login_screen = Toplevel(self.main_screen)
        self.login_screen.title("Login")
        self.login_screen.geometry("200x150")

        Label(self.login_screen, text="Please enter your details").pack()

        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Username * ").pack()
        self.username_login_entry = Entry(self.login_screen, textvariable=self.username)
        self.username_login_entry.pack()

        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Start authentication", width=20, height=1, command=self._start_auth).pack()

    def _start_auth(self):
        username = self.username.get()

        self.username_login_entry.delete(0, END)  # TODO: what for?

        if not self.authenticator.check_user_exists(username):
            self._user_not_found()
            return

        auth_methods = self.authenticator.get_authentication_methods(username)

        authentication_classes = {"grid": GridPhotosScreen, "pixels": PixelsScreen, "text": TextScreen}

        for auth_method in ["text", "grid", "pixels"]:  # TODO: move to const
            if auth_method in auth_methods:
                screen = authentication_classes[auth_method](self)
                screen.create(username)

                self.login_screen.wait_window(screen.screen)

        if login_success:
            self._login_success()

    def _login_success(self):
        self.login_success_screen = Toplevel(self.login_screen)
        self.login_success_screen.title("Success")
        self.login_success_screen.geometry("128x128")
        Label(self.login_success_screen, text="Login Success").pack()
        Button(self.login_success_screen, text="OK", command=self._delete_login_success).pack()

    def _user_not_found(self):
        self.user_not_found_screen = Toplevel(self.login_screen)
        self.user_not_found_screen.title("Success")
        self.user_not_found_screen.geometry("150x100")
        Label(self.user_not_found_screen, text="User Not Found").pack()
        Button(self.user_not_found_screen, text="OK", command=self._delete_user_not_found_screen).pack()

    def _delete_login_success(self):
        self.login_success_screen.destroy()
        self.login_screen.destroy()

    def _delete_user_not_found_screen(self):
        self.user_not_found_screen.destroy()
