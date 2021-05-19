from tkinter import StringVar, Toplevel, Label, Entry, Button, END
from PIL import Image, ImageTk

GRID_PHOTO_PATH = r"assets\grid_photos"


class Login(object):
    def __init__(self, auth, main_screen):
        self.main_screen = main_screen
        self.login_screen = None
        self.user_not_found_screen = None
        self.password_not_recog_screen = None
        self.login_success_screen = None
        self.username_login_entry = None
        self.password_login_entry = None

        self.username = StringVar()
        self.password = StringVar()

        self.auth = auth

        self.grid_password = ""

    def login_user(self):
        self.login_screen = Toplevel(self.main_screen)
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")

        Label(self.login_screen, text="Please enter details below to login").pack()

        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Username * ").pack()
        self.username_login_entry = Entry(self.login_screen, textvariable=self.username)
        self.username_login_entry.pack()

        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Password * ").pack()
        self.password_login_entry = Entry(self.login_screen, textvariable=self.password, show='*')
        self.password_login_entry.pack()

        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Login", width=10, height=1, command=self._text_login_verify).pack()

    def _text_login_verify(self):
        username = self.username.get()
        password = self.password.get()
        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

        print(username)
        print(password)

        if not self.auth.check_user_exists(username):
            self._user_not_found()
        elif self.auth.verify_user_text_password(username, password):
            self._grid_login(username)
        else:
            self._password_not_recognised()

    def _login_success(self):
        self.login_success_screen = Toplevel(self.login_screen)
        self.login_success_screen.title("Success")
        self.login_success_screen.geometry("128x128")
        Label(self.login_success_screen, text="Login Success").pack()
        Button(self.login_success_screen, text="OK", command=self._delete_login_success).pack()

    def _grid_login_verify(self, username):
        if self.auth.verify_user_grid_password(username, self.grid_password):
            self._login_success()
        else:
            self.grid_password = ""
            self._password_not_recognised()

    def _build_grid_password(self, i):
        self.grid_password += str(i)

    def _add_photo_button(self, photo_name, screen, row, column, i):
        image = Image.open(GRID_PHOTO_PATH + "\\" + photo_name)
        photo = ImageTk.PhotoImage(image)
        label = Button(screen, command=lambda: self._build_grid_password(i), image=photo)
        label.image = photo
        label.grid(row=row, column=column)

    def _grid_login(self, username):
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

        button = Button(self.photo_grid_screen, text="Login", width=10, height=1,
                        command=lambda: self._grid_login_verify(username))
        label=Label(self.photo_grid_screen, text="")
        label.grid(row=3, column=1)
        button.grid(row=4, column=1)

    def _password_not_recognised(self):
        self.password_not_recog_screen = Toplevel(self.login_screen)
        self.password_not_recog_screen.title("Invalid password")
        self.password_not_recog_screen.geometry("150x100")
        Label(self.password_not_recog_screen, text="Invalid Password ").pack()
        Button(self.password_not_recog_screen, text="OK", command=self._delete_password_not_recognised).pack()

    def _user_not_found(self):
        self.user_not_found_screen = Toplevel(self.login_screen)
        self.user_not_found_screen.title("Success")
        self.user_not_found_screen.geometry("150x100")
        Label(self.user_not_found_screen, text="User Not Found").pack()
        Button(self.user_not_found_screen, text="OK", command=self._delete_user_not_found_screen).pack()

    def _delete_login_success(self):
        self.login_success_screen.destroy()
        self.photo_grid_screen.destroy()
        self.login_screen.destroy()

    def _delete_password_not_recognised(self):
        self.password_not_recog_screen.destroy()

    def _delete_user_not_found_screen(self):
        self.user_not_found_screen.destroy()
