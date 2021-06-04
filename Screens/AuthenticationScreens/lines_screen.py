from tkinter import *

LENGTH = 500
current = None

number_of_lines = 0

from tkinter import Label, Entry, Toplevel, END, StringVar, Button

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import IAuthScreen
from Utils.tkinter_utils import destroy_screens


class LinesScreen(IAuthScreen):
    def __init__(self, login):
        super().__init__(login)

        self.lines_screen = None

        self._password = StringVar()
        self._password_login_entry = None

    @property
    def screen(self):
        return self.lines_screen

    def create(self, username, email):
        self.lines_screen = Toplevel(self.login_screen)
        self.lines_screen.title("Lines")
        self.lines_screen.geometry("250x150")

        drawing_area = Canvas(self.lines_screen, width=LENGTH, height=LENGTH, bg='white')
        drawing_area.pack()
        self.draw_grid(drawing_area)
        drawing_area.bind("<Escape>", self._reset)
        drawing_area.bind("<Motion>", self._motion)
        drawing_area.bind("<ButtonPress-1>", self._mouse_down)
        drawing_area.bind("<Double-Button-1>", self._finished)

        Label(self.lines_screen, text="").pack()
        Button(self.lines_screen, text="Finished", width=20, height=1,
               command=lambda: self._verify(username, email)).pack()

    def _verify(self, username, email):
        password = self._password.get()
        self._password_login_entry.delete(0, END)

        if self.authenticator.verify_user_text_password(username, password):
            login.login_success = True
            destroy_screens(self.lines_screen)
        else:
            self._login_failed(username, email)

    def draw_grid(self, drawing_area, line_distance=LENGTH // 4):
        for x in range(line_distance, LENGTH, line_distance):
            drawing_area.create_line(x, 0, x, LENGTH, fill="#d3d3d3")

        for y in range(line_distance, LENGTH, line_distance):
            drawing_area.create_line(0, y, LENGTH, y, fill="#d3d3d3")

    def _finished(self, event):
        print("Finished")

    def _reset(self, event):
        global current
        current = None

    def _mouse_down(self, event):
        global current
        global number_of_lines

        event.widget.focus_set()  # so escape key will work

        if current is None:
            # the new line starts where the user clicked
            x0 = event.x
            y0 = event.y

        else:
            # the new line starts at the end of the previously
            # drawn line
            coords = event.widget.coords(current)
            x0 = coords[2]
            y0 = coords[3]

        # create the new line
        number_of_lines += 1
        current = event.widget.create_line(x0, y0, event.x, event.y)

    def _motion(self,   event):
        if current:
            # modify the current line by changing the end coordinates
            # to be the current mouse position
            coords = event.widget.coords(current)
            coords[2] = event.x
            coords[3] = event.y

            event.widget.coords(current, *coords)
