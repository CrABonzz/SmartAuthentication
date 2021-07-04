from tkinter import StringVar, Toplevel, Label, Button, Image

from PIL import Image, ImageTk

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import AuthScreen
from Utils.common import GRID_PHOTOS
from Utils.password_utils import random_numbers
from Utils.tkinter_utils import destroy_screens, add_screen

GRID_PHOTO_PATH = r"assets\grid_photos"


class GridPhotosScreen(AuthScreen):
    def __init__(self, auth):
        super().__init__(auth)

        self.photo_grid_screen = None
        self.grid_password = ""
        self._finished_button_text = StringVar()
        self._number_of_clicks = 0
        self._finished_button_text.set("Finished (0 Clicks)")

    @property
    def screen(self):
        return self.photo_grid_screen

    @property
    def password(self):
        return self.grid_password

    def _reset_fields(self):
        self._number_of_clicks = 0
        self.grid_password = ""

    def _create_screen(self, screen, photos_ids, button_command):
        self._reset_fields()

        self.photo_grid_screen = add_screen(screen, "Photo grid", "400x460")

        for index, photo_id in enumerate(photos_ids):
            self._add_photo_button(self.photo_grid_screen, index, photo_id)

        button = Button(self.photo_grid_screen, textvariable=self._finished_button_text, width=15, height=1,
                        command=button_command)
        label = Label(self.photo_grid_screen, text="")
        label.grid(row=3, column=1)
        button.grid(row=4, column=1)

    def handle_register(self, register_screen):
        photos_ids = random_numbers(amount=9)

        button_command = lambda: destroy_screens(self.photo_grid_screen)

        self._create_screen(register_screen, photos_ids, button_command)

        return photos_ids

    def handle_login(self, login_screen, username, email):
        button_command = lambda: self._verify(login_screen, username, email)

        photos_ids = self.authenticator.get_photos_ids(username, email)
        self._create_screen(login_screen, photos_ids, button_command)

    def _verify(self, login_screen, username, email):
        if self.authenticator.verify_user_grid_password(username, self.grid_password):
            login.login_success = True
            destroy_screens(self.photo_grid_screen)
        else:
            self._reset_fields()
            self._login_failed(login_screen, username, email)

    def _add_photo_button(self, screen, index, photo_id):
        """
        Add one box
        """
        image = Image.open(GRID_PHOTO_PATH + "\\" + GRID_PHOTOS[photo_id])
        photo = ImageTk.PhotoImage(image)
        label = Button(screen, command=lambda: self._build_grid_password(photo_id), image=photo)

        label.image = photo
        label.grid(row=index // 3, column=index % 3)

    def _build_grid_password(self, i):
        self.grid_password += str(i) + ","
        self._number_of_clicks += 1
        self._finished_button_text.set("Finished (" + str(self._number_of_clicks) + " Clicks)")
