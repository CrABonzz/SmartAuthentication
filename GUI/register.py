import binascii
import hashlib
import json
from tkinter import StringVar, Toplevel, Label, Entry, Button, END, Checkbutton, LEFT, BOTTOM, W, BooleanVar, S, \
    DISABLED
from PIL import Image, ImageTk

from GUI.login import GRID_PHOTO_PATH
from Utils.common import HASH_ITERATIONS_AMOUNT
from Utils.general_utils import random_salt


class Register(object):
    def __init__(self, auth, main_screen):
        self.auth = auth
        self.main_screen = main_screen
        self.register_screen = None

        self.username = StringVar()
        self.text_password = StringVar()
        self.username_entry = None
        self.text_password_entry = None
        self.photo_grid_screen = None

        self.grid_password = ""  # TODO: store hidden

    def register_user(self):
        self.register_screen = Toplevel(self.main_screen)
        self.register_screen.title("Register")
        self.register_screen.geometry("300x250")

        Label(self.register_screen, text="Please enter details below", bg="blue").pack()
        Label(self.register_screen, text="").pack()

        username_label = Label(self.register_screen, text="Username * ")
        username_label.pack()

        self.username_entry = Entry(self.register_screen, textvariable=self.username)
        self.username_entry.pack()

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

        todo_auth = BooleanVar()
        check_button = Checkbutton(self.register_screen, text="TODO", variable=todo_auth)
        check_button.pack(side=LEFT)

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue",
               command=lambda: self._register_user(grid_auth, todo_auth)).pack(side=BOTTOM, anchor=S)

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
        self.photo_grid_screen = Toplevel(self.register_screen)
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

        button = Button(self.photo_grid_screen, text="Finish", command=self._delete_grid_registering, width=10,
                        height=1)
        label = Label(self.photo_grid_screen, text="")
        label.grid(row=3, column=1)
        button.grid(row=4, column=1)

    def _register_user(self, grid_auth, todo_auth):
        if grid_auth.get():
            self._create_grid_password()
            self.register_screen.wait_window(self.photo_grid_screen)
            grid_password = self._hash_password(self.grid_password).decode('ascii')
        else:
            grid_password = ""

        username = self.username.get()

        new_user = {
            "user": username,
            "passwords": {
                "text": self._hash_password(self.text_password.get()).decode('ascii'),
                "grid": grid_password
            }
        }

        with open(r"assets\users.json", "r+") as users_file:
            all_users = json.load(users_file)
            all_users["users"].append(new_user)

            users_file.seek(0)
            users_file.truncate()
            json.dump(all_users, users_file)

        # self.username_entry.delete(0, END)
        # self.text_password_entry.delete(0, END)

        self._register_success()

    def _register_success(self):
        self.auth.update_users_file()

        self.register_success_screen = Toplevel()
        self.register_success_screen.title("Success")
        self.register_success_screen.geometry("128x128")
        Label(self.register_success_screen, text="Register Success").pack()
        Button(self.register_success_screen, text="OK", command=self._delete_register_registering).pack()

    def _delete_grid_registering(self):
        self.photo_grid_screen.destroy()

    def _delete_register_registering(self):
        self.register_screen.destroy()
        self.register_success_screen.destroy()