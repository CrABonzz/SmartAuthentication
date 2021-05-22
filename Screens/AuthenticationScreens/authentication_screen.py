from abc import ABCMeta, abstractmethod
from tkinter import StringVar, Toplevel, Label, Entry, Button, END, RAISED


class IAuthScreen(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, login):
        super(IAuthScreen, self).__init__()
        self.login_screen = login.login_screen
        self.authenticator = login.authenticator

        self.password_not_recog_screen = None

    @abstractmethod
    def screen(self):
        pass

    @abstractmethod
    def create(self, username):
        pass

    # TODO: call it when needed
    def _password_not_recognised(self):
        self.password_not_recog_screen = Toplevel(self.login_screen)
        self.password_not_recog_screen.title("Invalid password")
        self.password_not_recog_screen.geometry("150x100")
        Label(self.password_not_recog_screen, text="Invalid Password ").pack()
        Button(self.password_not_recog_screen, text="OK", command=self._delete_password_not_recognised).pack()

    def _delete_password_not_recognised(self):
        self.password_not_recog_screen.destroy()
