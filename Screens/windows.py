from tkinter import *

from Authentication.authenticator import Authenticator
from Screens.login import Login
from Screens.register import Register


class MainPage(object):
    def __init__(self):
        self.main_screen = Tk()

        self.main_screen.geometry("300x250")
        self.main_screen.title("Main page")

        auth = Authenticator()

        self.login = Login(auth, self.main_screen)
        self.register = Register(auth, self.main_screen)

        Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command=self.login.login_window).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.register.register_user).pack()

    def run(self):
        self.main_screen.mainloop()
