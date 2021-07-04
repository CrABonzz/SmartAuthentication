from Screens import login
from Screens.AuthenticationScreens.authentication_screen import AuthScreen
from tkinter import StringVar, Toplevel, Label, Entry, Button, END, RAISED, BOTTOM, TOP
from PIL import Image, ImageTk

from Utils.tkinter_utils import destroy_screens, add_screen

PIXEL_PHOTO_PATH = r"assets\pixels_photos"


class PixelsScreen(AuthScreen):
    def __init__(self, auth):
        super().__init__(auth)

        self.pixels_screen = None

        self._clicks = []

    @property
    def screen(self):
        return self.pixels_screen

    @property
    def password(self):
        return self._clicks

    def _reset_fields(self):
        self._clicks = []

    def _create(self, screen, button_command, pixels_click_command):
        self._reset_fields()
        self.pixels_screen = add_screen(screen, "Pixels", "750x550")

        photo = ImageTk.PhotoImage(Image.open(PIXEL_PHOTO_PATH + "\\" + "switzerland.jpg"))
        label = Button(self.pixels_screen, image=photo)
        label.image = photo
        label.bind("<Button-1>", pixels_click_command)
        label.pack(side=TOP)

        button = Button(self.pixels_screen, text="Finished", width=10, height=1,
                        command=button_command)
        button.pack()

    def handle_register(self, register_screen):
        button_command = lambda: destroy_screens(self.pixels_screen)

        self._create(register_screen, button_command, self._pixels_click_register)

    def handle_login(self, login_screen, username, email):
        button_command = lambda: self._verify(login_screen, username, email)

        self._create(login_screen, button_command, self._pixels_click_login)

    def _verify(self, login_screen, username, email):
        if self.authenticator.verify_pixels_password(username, self._clicks):
            login.login_success = True
            destroy_screens(self.pixels_screen)
        else:
            self._reset_fields()
            self._login_failed(login_screen, username, email)

    def _pixels_click_login(self, coordinates):
        self._clicks += [(coordinates.x, coordinates.y)]

    def _pixels_click_register(self, coordinates):
        self._clicks += [str(coordinates.x) + "-" + str(coordinates.y) + ", "]


