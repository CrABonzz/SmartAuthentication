from tkinter import StringVar, Toplevel, Label, Entry, Button, END
from PIL import Image, ImageTk

GRID_PHOTO_PATH = r"assets\grid_photos"

from Authentication.Authenticate import Authenticate


class Login(object):
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.login_screen = None
        self.user_not_found_screen = None
        self.password_not_recog_screen = None
        self.login_success_screen = None
        self.username_login_entry = None
        self.password_login_entry = None

        self.username = StringVar()
        self.password = StringVar()

        self.auth = Authenticate()

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
        Button(self.login_screen, text="Login", width=10, height=1, command=self._login_verify).pack()

    def _login_verify(self):
        username = self.username.get()
        password = self.password.get()
        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

        print(username)
        print(password)
        self.auth.verify_user(username, password)

        if not self.auth.check_user_exists(username):
            self._user_not_found()
        elif self.auth.verify_user(username, password):
            self._login_success()
        else:
            self._password_not_recognised()

    def print_junk(self, i):
        print("Some junk: " + str(i))

    def _login_success(self):
        self.login_success_screen = Toplevel(self.login_screen)
        self.login_success_screen.title("Success")
        self.login_success_screen.geometry("520x520")
        # Label(self.login_success_screen, text="Login Success").pack()
        # Button(self.login_success_screen, text="OK", command=self._delete_login_success).pack()

        image = Image.open(GRID_PHOTO_PATH + "\\number1.png")
        photo = ImageTk.PhotoImage(image)
        label = Button(self.login_success_screen, command=lambda: self.print_junk(1), image=photo)
        label.image = photo
        label.grid(row=0, column=0)

        image = Image.open(GRID_PHOTO_PATH + "\\number2.png")
        photo = ImageTk.PhotoImage(image)
        label = Button(self.login_success_screen, command=lambda: self.print_junk(2), image=photo)
        label.image = photo
        label.grid(row=0, column=1)

        image = Image.open(GRID_PHOTO_PATH + "\\number3.png")
        photo = ImageTk.PhotoImage(image)
        label = Button(self.login_success_screen, command=lambda: self.print_junk(3), image=photo)
        label.image = photo
        label.grid(row=1, column=0)

        image = Image.open(GRID_PHOTO_PATH + "\\number4.png")
        photo = ImageTk.PhotoImage(image)
        label = Button(self.login_success_screen, command=lambda: self.print_junk(4), image=photo)
        label.image = photo
        label.grid(row=1, column=1)

    def _password_not_recognised(self):
        self.password_not_recog_screen = Toplevel(self.login_screen)
        self.password_not_recog_screen.title("Success")
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

    def _delete_password_not_recognised(self):
        self.password_not_recog_screen.destroy()

    def _delete_user_not_found_screen(self):
        self.user_not_found_screen.destroy()
