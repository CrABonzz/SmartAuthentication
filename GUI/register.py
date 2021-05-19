import json
from tkinter import StringVar, Toplevel, Label, Entry, Button, END


class Register(object):
    def __init__(self, auth, main_screen):
        self.auth = auth
        self.main_screen = main_screen
        self.register_screen = None

        self.username = StringVar()
        self.text_password = StringVar()
        self.username_entry = None
        self.text_password_entry = None

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

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue", command=self._register_user).pack()

    def _register_user(self):
        username_info = self.username.get()
        text_password = self.text_password.get()

        new_user = {
            "user": username_info,
            "passwords": {
                "text": text_password,
                "grid": "2341"
            }
        }

        with open(r"assets\users.json", "r+") as users_file:
            all_users = json.load(users_file)
            all_users["users"].append(new_user)

            users_file.seek(0)
            users_file.truncate()
            json.dump(all_users, users_file)

        self.username_entry.delete(0, END)
        self.text_password_entry.delete(0, END)

        self.auth.update_users_file()

        Label(self.register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
