from tkinter import StringVar, Toplevel, Label, Button, Image

from PIL import Image, ImageTk

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import IAuthScreen
from Utils.common import GRID_PHOTOS
from Utils.tkinter_utils import destroy_screens

GRID_PHOTO_PATH = r"assets\grid_photos"


class GridPhotosScreen(IAuthScreen):
    def __init__(self, login):
        super().__init__(login)

        self.photo_grid_screen = None
        self.grid_password = ""
        self._finished_button_text = StringVar()
        self._number_of_clikcs = 0
        self._finished_button_text.set("Finished (0 Clicks)")

    @property
    def screen(self):
        return self.photo_grid_screen

    def create(self, username, email):
        self.photo_grid_screen = Toplevel(self.login_screen)
        self.photo_grid_screen.title("Photo grid")
        self.photo_grid_screen.geometry("400x460")

        photos_ids = self.authenticator.get_photos_ids(username, email)

        for index, photo_id in enumerate(photos_ids):
            self._add_photo_button(self.photo_grid_screen, index, photo_id)

        button = Button(self.photo_grid_screen, textvariable=self._finished_button_text, width=15, height=1,
                        command=lambda: self._verify(username, email))
        label = Label(self.photo_grid_screen, text="")
        label.grid(row=3, column=1)
        button.grid(row=4, column=1)

    def _verify(self, username, email):
        if self.authenticator.verify_user_grid_password(username, self.grid_password):
            login.login_success = True
            destroy_screens(self.photo_grid_screen)
        else:
            self.grid_password = ""
            self._number_of_clikcs = 0
            self._login_failed(username, email)

    def _add_photo_button(self, screen, index, photo_id):
        image = Image.open(GRID_PHOTO_PATH + "\\" + GRID_PHOTOS[photo_id])
        photo = ImageTk.PhotoImage(image)
        label = Button(screen, command=lambda: self._build_grid_password(photo_id), image=photo)

        label.image = photo
        label.grid(row=index // 3, column=index % 3)

    def _build_grid_password(self, i):
        self.grid_password += str(i) + ","
        self._number_of_clikcs += 1
        self._finished_button_text.set("Finished (" + str(self._number_of_clikcs) + " Clicks)")
