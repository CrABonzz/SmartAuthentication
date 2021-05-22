from tkinter import StringVar, Toplevel, Label, Entry, Button, END, RAISED, Image
from PIL import Image, ImageTk

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import IAuthScreen

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

    def create(self, username):
        self.photo_grid_screen = Toplevel(self.login_screen)
        self.photo_grid_screen.title("Photo grid")
        self.photo_grid_screen.geometry("400x460")

        self._add_photo_button("delicious.png", self.photo_grid_screen, 0, 0, 0)
        self._add_photo_button("digg.png", self.photo_grid_screen, 0, 1, 1)
        self._add_photo_button("furl.png", self.photo_grid_screen, 0, 2, 2)
        self._add_photo_button("flickr.png", self.photo_grid_screen, 1, 0, 3)
        self._add_photo_button("reddit.png", self.photo_grid_screen, 1, 1, 4)
        self._add_photo_button("rss.png", self.photo_grid_screen, 1, 2, 5)
        self._add_photo_button("stumbleupon.png", self.photo_grid_screen, 2, 0, 6)
        self._add_photo_button("yahoo.png", self.photo_grid_screen, 2, 1, 7)
        self._add_photo_button("youtube.png", self.photo_grid_screen, 2, 2, 8)

        button = Button(self.photo_grid_screen, textvariable=self._finished_button_text, width=15, height=1,
                        command=lambda: self._verify(username))
        label = Label(self.photo_grid_screen, text="")
        label.grid(row=3, column=1)
        button.grid(row=4, column=1)

    def _verify(self, username):
        if self.authenticator.verify_user_grid_password(username, self.grid_password):
            self._delete_photo_grid_screen()
        else:
            self.grid_password = ""
            login.login_success = False
            self._password_not_recognised()

    def _add_photo_button(self, photo_name, screen, row, column, i):
        image = Image.open(GRID_PHOTO_PATH + "\\" + photo_name)
        photo = ImageTk.PhotoImage(image)
        label = Button(screen, command=lambda: self._build_grid_password(i), image=photo)

        label.image = photo  # TODO: needed?
        label.grid(row=row, column=column)

    def _build_grid_password(self, i):
        self.grid_password += str(i)
        self._number_of_clikcs += 1
        self._finished_button_text.set("Finished (" + str(self._number_of_clikcs) + " Clicks)")

    def _delete_photo_grid_screen(self):
        self.photo_grid_screen.destroy()
