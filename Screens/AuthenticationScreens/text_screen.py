from tkinter import Label, Entry, Toplevel, END, StringVar, Button

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import IAuthScreen
from Utils.tkinter_utils import destroy_screens


class TextScreen(IAuthScreen):
    def __init__(self, login):
        super().__init__(login)

        self.text_screen = None

        self._password = StringVar()
        self._password_login_entry = None

    @property
    def screen(self):
        return self.text_screen

    def create(self, username, email):
        self.text_screen = Toplevel(self.login_screen)
        self.text_screen.title("Photo grid")
        self.text_screen.geometry("250x150")

        Label(self.text_screen, text="").pack()
        Label(self.text_screen, text="Text password").pack()
        self._password_login_entry = Entry(self.text_screen, textvariable=self._password, show='*')
        self._password_login_entry.pack()

        Label(self.text_screen, text="").pack()
        Button(self.text_screen, text="Finished", width=20, height=1,
               command=lambda: self._verify(username, email)).pack()

    def _verify(self, username, email):
        password = self._password.get()
        self._password_login_entry.delete(0, END)

        if self.authenticator.verify_user_text_password(username, password):
            login.login_success = True
            destroy_screens(self.text_screen)
        else:
            self._login_failed(username, email)
