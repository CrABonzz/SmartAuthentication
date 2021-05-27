from Screens import login
from Screens.AuthenticationScreens.authentication_screen import IAuthScreen
from tkinter import StringVar, Toplevel, Label, Entry, Button, END, RAISED, BOTTOM, TOP
from PIL import Image, ImageTk

from Utils.tkinter_utils import destroy_screens

PIXEL_PHOTO_PATH = r"assets\pixels_photos"


class PixelsScreen(IAuthScreen):
    def __init__(self, login):
        super().__init__(login)

        self.pixels_screen = None

        self._clicks = []

    @property
    def screen(self):
        return self.pixels_screen

    def create(self, username, email):
        self.pixels_screen = Toplevel(self.login_screen)
        self.pixels_screen.title("Pixels")
        self.pixels_screen.geometry("750x550")

        photo = ImageTk.PhotoImage(Image.open(PIXEL_PHOTO_PATH + "\\" + "switzerland.jpg"))
        label = Button(self.pixels_screen, image=photo)
        label.image = photo
        label.bind("<Button-1>", self._pixels_click)
        label.pack(side=TOP)

        button = Button(self.pixels_screen, text="Finished", width=10, height=1,
                        command=lambda: self._verify(username, email))
        button.pack()

    def _verify(self, username, email):
        if self.authenticator.verify_pixels_password(username, self._clicks):
            destroy_screens(self.pixels_screen)
        else:
            login.login_success = False
            self._clicks = []
            self._notify_user_mail(username, email)
            self._password_not_recognised()

    def _pixels_click(self, coordinates):
        self._clicks += [(coordinates.x, coordinates.y)]
