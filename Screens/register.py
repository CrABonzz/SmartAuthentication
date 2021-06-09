from tkinter import StringVar, Label, Entry, Button, END, Checkbutton, LEFT, BOTTOM, W, BooleanVar, S, \
    DISABLED

from validate_email import validate_email

from Utils.password_utils import hash_password
from Utils.json_utils import add_new_user
from Utils.tkinter_utils import add_entry, add_screen, info_screen


class Register(object):
    def __init__(self, auth, main_screen, photo_grid_screen, text_screen, pixels_screen, lines_screen):
        self.auth = auth
        self.main_screen = main_screen
        self.photo_grid_screen = photo_grid_screen
        self.text_screen = text_screen
        self.pixels_screen = pixels_screen
        self.lines_screen = lines_screen

        self.register_screen = None
        self.username = StringVar()
        self.email = StringVar()
        self.text_password = StringVar()
        self.username_entry = None
        self.email_entry = None
        self.text_password_entry = None

    def add_new_user(self):
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

        lines_auth = BooleanVar()
        check_button = Checkbutton(self.register_screen, text="Lines", onvalue=True, offvalue=False,
                                   variable=lines_auth)
        check_button.pack(side=LEFT)

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue",
               command=lambda: self._register_user(grid_auth, pixels_auth, lines_auth)).pack(side=BOTTOM, anchor=S)

    def _register_user(self, grid_auth, pixels_auth, lines_auth):
        username = self.username.get()
        email = self.email.get()
        text_password = self.text_password.get()

        if not self._check_fields_validaty(username, email, text_password):
            return

        grid_password, photos_ids = self._grid_auth(grid_auth)
        pixels_password = self._pixels_auth(pixels_auth)
        lines_password = self._lines_auth(lines_auth)

        # The format of the user data in the json file on the disk
        new_user = {
            "user": username,
            "email": email,
            "count_failed_tries": 0,
            "blocked": False,
            "grid_photos_ids": photos_ids,
            "passwords": {
                "text": hash_password(text_password),
                "grid": grid_password,
                "pixels": pixels_password,
                "lines": lines_password,
            }
        }

        add_new_user(new_user)
        self.username_entry.delete(0, END)
        self.text_password_entry.delete(0, END)
        self.email_entry.delete(0, END)

        self.auth.update_users_file()
        info_screen(self.register_screen, "Register success", "128x100")

    def _check_fields_validaty(self, username, email, password):
        """
        The that the user data is acceptable
        """
        password_mismatch = self.auth.password_strong(password)

        if password_mismatch != "":
            # TODO: undo in production
            # info_screen(self.register_screen, "Password isn't strong", "300x200", password_mismatch)
            # return False
            pass

        if not validate_email(email):
            # TODO: undo in production
            # info_screen(self.register_screen, "Email isn't valid", "200x100")
            # return False
            pass

        user_exists, _ = self.auth.check_user_exists(username, email)
        if user_exists:
            info_screen(self.register_screen, "User already exists", "300x200",
                        "User with this username or email already exists")
            return False

        return True

    def _grid_auth(self, grid_auth):
        photos_ids, grid_password = [], ""

        if grid_auth.get():
            photos_ids = self.photo_grid_screen.handle_register(self.register_screen)
            self.register_screen.wait_window(self.photo_grid_screen.screen)
            grid_password = hash_password(self.photo_grid_screen.password)

        return grid_password, photos_ids

    def _pixels_auth(self, pixels_auth):
        pixels_password = ""

        if pixels_auth.get():
            self.pixels_screen.handle_register(self.register_screen)
            self.register_screen.wait_window(self.pixels_screen.screen)
            pixels_password = self.pixels_screen.password

        return pixels_password

    def _lines_auth(self, lines_auth):
        lines_password = ""

        if lines_auth.get():
            self.lines_screen.handle_register(self.register_screen)
            self.register_screen.wait_window(self.lines_screen.screen)
            lines_password = hash_password(self.lines_screen.password)

        return lines_password
