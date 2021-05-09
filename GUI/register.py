from tkinter import StringVar, Toplevel, Label, Entry, Button


class Register(object):
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.register_screen = None

        self.username = StringVar()
        self.password = StringVar()

    def register_user(self):
        self.register_screen = Toplevel(self.main_screen)
        self.register_screen.title("Register")
        self.register_screen.geometry("300x250")

        Label(self.register_screen, text="Please enter details below", bg="blue").pack()
        Label(self.register_screen, text="").pack()

        username_label = Label(self.register_screen, text="Username * ")
        username_label.pack()

        username_entry = Entry(self.register_screen, textvariable=self.username)
        username_entry.pack()

        password_label = Label(self.register_screen, text="Password * ")
        password_label.pack()

        password_entry = Entry(self.register_screen, textvariable=self.password, show='*')
        password_entry.pack()

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue", command=self._register_user).pack()

    def _register_user(self):
        username_info = self.username.get()
        password_info = self.password.get()

        print("Register this user")

        # username_entry.delete(0, END)
        # password_entry.delete(0, END)

        Label(self.register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
