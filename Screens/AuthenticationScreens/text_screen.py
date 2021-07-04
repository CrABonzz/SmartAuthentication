from tkinter import Label, Entry, Toplevel, END, StringVar, Button

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import AuthScreen
from Utils.tkinter_utils import destroy_screens, add_screen


class TextScreen(AuthScreen):
    def __init__(self, auth):
        super().__init__(auth)

        self.text_screen = None

        self._password = StringVar()
        self._password_login_entry = None

    @property
    def screen(self):
        return self.text_screen

    @property
    def password(self):
        return self.password

    def _create_screen(self, screen, button_command):
        self.text_screen = add_screen(screen, "Text", "250x150")

        Label(self.text_screen, text="").pack()
        Label(self.text_screen, text="Text password").pack()
        self._password_login_entry = Entry(self.text_screen, textvariable=self._password, show='*')
        self._password_login_entry.pack()

        Label(self.text_screen, text="").pack()
        Button(self.text_screen, text="Finished", width=20, height=1,
               command=button_command).pack()

    def handle_register(self, register_screen):
        pass

    def handle_login(self, login_screen, username, email):
        button_command = lambda: self._verify(login_screen, username, email)
        self._create_screen(login_screen, button_command)

    def _verify(self, login_screen, username, email):
        password = self._password.get()
        self._password_login_entry.delete(0, END)

        if self.authenticator.verify_user_text_password(username, password):
            login.login_success = True
            destroy_screens(self.text_screen)
        else:
            self._login_failed(login_screen, username, email)
