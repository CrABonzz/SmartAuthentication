from tkinter import *

from GUI.login import Login
from GUI.register import Register


class MainPage(object):
    def __init__(self):
        self.main_screen = Tk()

        self.main_screen.geometry("300x250")
        self.main_screen.title("Main page")

        self.login = Login(self.main_screen)
        self.register = Register(self.main_screen)

        Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command=self.login._login_success).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.register.register_user).pack()

    def run(self):
        self.main_screen.mainloop()
