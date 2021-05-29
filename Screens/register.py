import binascii
import hashlib
from tkinter import StringVar, Label, Entry, Button, END, Checkbutton, LEFT, BOTTOM, W, BooleanVar, S, \
    DISABLED, TOP

from PIL import Image, ImageTk

from Screens.AuthenticationScreens.grid_photos_screen import GRID_PHOTO_PATH
from Screens.AuthenticationScreens.pixels_screen import PIXEL_PHOTO_PATH
from Utils.common import HASH_ITERATIONS_AMOUNT
from Utils.general_utils import random_salt
from Utils.json_utils import add_new_user
from Utils.tkinter_utils import add_entry, add_screen, destroy_screens, info_screen


class Register(object):
    def __init__(self, auth, main_screen):
        self.auth = auth
        self.main_screen = main_screen
        self.register_screen = None

        self.username = StringVar()
        self.email = StringVar()
        self.text_password = StringVar()
        self.username_entry = None
        self.email_entry = None
        self.text_password_entry = None
        self.photo_grid_screen = None
        self.pixels_screen = None

        self.grid_password = ""  # TODO: store hidden
        self._clicks = ""

    # TODO: rename method
    def register_user(self):
        self.register_screen = add_screen(self.main_screen, "Register", "300x250")

        Label(self.register_screen, text="Please enter details below", bg="blue").pack()
        Label(self.register_screen, text="").pack()

        self.username_entry = add_entry(self.register_screen, "Username", self.username)
        self.email_entry = add_entry(self.register_screen, "Email", self.email)

        password_label = Label(self.register_screen, text="Password * ")
        password_label.pack()

        self.text_password_entry = Entry(self.register_screen, textvariable=self.text_password, show='*')
        self.text_password_entry.pack()

        check_button = Checkbutton(self.register_screen, text="Text", state=DISABLED)
        check_button.select()
        check_button.pack(anchor=W, side=LEFT)

        grid_auth = BooleanVar()
        check_button = Checkbutton(self.register_screen, text="Grid", onvalue=True, offvalue=False, variable=grid_auth)
        check_button.pack(side=LEFT)

        pixels_auth = BooleanVar()
        check_button = Checkbutton(self.register_screen, text="Pixels", variable=pixels_auth)
        check_button.pack(side=LEFT)

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue",
               command=lambda: self._register_user(grid_auth, pixels_auth)).pack(side=BOTTOM, anchor=S)

    def _hash_password(self, password):
        salt = random_salt()

        hashed_password = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt,
            HASH_ITERATIONS_AMOUNT
        )

        return salt + binascii.hexlify(hashed_password)

    def _build_grid_password(self, i):
        self.grid_password += str(i)

    def _add_photo_button(self, photo_name, screen, row, column, i):
        image = Image.open(GRID_PHOTO_PATH + "\\" + photo_name)
        photo = ImageTk.PhotoImage(image)
        label = Button(screen, command=lambda: self._build_grid_password(i), image=photo)
        label.image = photo
        label.grid(row=row, column=column)

    def _create_grid_password(self):
        self.photo_grid_screen = add_screen(self.register_screen, "Photo grid", "400x460")

        # TODO: add more photos and ids
        self._add_photo_button("delicious.png", self.photo_grid_screen, 0, 0, 0)
        self._add_photo_button("digg.png", self.photo_grid_screen, 0, 1, 1)
        self._add_photo_button("furl.png", self.photo_grid_screen, 0, 2, 2)
        self._add_photo_button("flickr.png", self.photo_grid_screen, 1, 0, 3)
        self._add_photo_button("reddit.png", self.photo_grid_screen, 1, 1, 4)
        self._add_photo_button("rss.png", self.photo_grid_screen, 1, 2, 5)
        self._add_photo_button("stumbleupon.png", self.photo_grid_screen, 2, 0, 6)
        self._add_photo_button("yahoo.png", self.photo_grid_screen, 2, 1, 7)
        self._add_photo_button("youtube.png", self.photo_grid_screen, 2, 2, 8)

        button = Button(self.photo_grid_screen, text="Finish", command=lambda: destroy_screens(self.photo_grid_screen),
                        width=10,
                        height=1)
        label = Label(self.photo_grid_screen, text="")
        label.grid(row=3, column=1)
        button.grid(row=4, column=1)

    def _create_pixels_password(self):
        self.pixels_screen = add_screen(self.register_screen, "Pixels", "750x550")

        photo = ImageTk.PhotoImage(Image.open(PIXEL_PHOTO_PATH + "\\" + "switzerland.jpg"))
        label = Button(self.pixels_screen, image=photo)
        label.image = photo
        label.bind("<Button-1>", self._pixels_click)
        label.pack(side=TOP)

        button = Button(self.pixels_screen, text="Finished", width=10, height=1,
                        command=lambda: destroy_screens(self.pixels_screen))
        button.pack()

    def _pixels_click(self, coordinates):
        self._clicks += str(coordinates.x) + "-" + str(coordinates.y) + ", "

    def _register_user(self, grid_auth, pixels_auth):
        text_password = self.text_password.get()
        password_mismatch = self.auth.password_strong(text_password)

        if password_mismatch != "":
            info_screen(self.register_screen, "Password isn't strong", "300x300", password_mismatch)
            return

        if grid_auth.get():
            self._create_grid_password()
            self.register_screen.wait_window(self.photo_grid_screen)
            grid_password = self._hash_password(self.grid_password).decode('ascii')
        else:
            grid_password = ""

        if pixels_auth.get():
            self._create_pixels_password()
            self.register_screen.wait_window(self.pixels_screen)
            pixels_password = str(self._clicks)
        else:
            pixels_password = ""

        new_user = {
            "user": self.username.get(),
            "email": self.email.get(),
            "count_failed_tries": 0,
            "blocked": False,
            "passwords": {
                "text": self._hash_password(text_password).decode('ascii'),
                "grid": grid_password,
                "pixels": pixels_password
            }
        }

        add_new_user(new_user)
        self.username_entry.delete(0, END)  # TODO: needed?

        self.auth.update_users_file()
        info_screen(self.register_screen, "Register success", "128x100")
