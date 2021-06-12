from tkinter import *

from Authentication.authenticator import Authenticator
from Screens.AuthenticationScreens.cube_screen import CubeScreen
from Screens.AuthenticationScreens.grid_photos_screen import GridPhotosScreen
from Screens.AuthenticationScreens.lines_screen import LinesScreen
from Screens.AuthenticationScreens.pixels_screen import PixelsScreen
from Screens.AuthenticationScreens.text_screen import TextScreen
from Screens.login import Login
from Screens.register import Register


class MainPage(object):
    def __init__(self):
        self.main_screen = Tk()

        self.main_screen.geometry("300x250")
        self.main_screen.title("Main page")

        auth = Authenticator()

        photo_grid_screen = GridPhotosScreen(auth)
        text_screen = TextScreen(auth)
        pixels_screen = PixelsScreen(auth)
        lines_screen = LinesScreen(auth)
        cube_screen = CubeScreen(auth)

        self.register = Register(auth, self.main_screen, photo_grid_screen, text_screen, pixels_screen, lines_screen,
                                 cube_screen)
        self.login = Login(auth, self.main_screen, photo_grid_screen, text_screen, pixels_screen, lines_screen)

        Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command=self.login.login_window).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.register.add_new_user).pack()

    def run(self):
        self.main_screen.mainloop()
