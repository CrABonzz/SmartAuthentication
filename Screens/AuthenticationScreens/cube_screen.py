from tkinter import Label, Button, Canvas, NW, PhotoImage

from PIL import Image, ImageTk
from Screens import login
from Screens.AuthenticationScreens.authentication_screen import IAuthScreen
from Screens.AuthenticationScreens.grid_photos_screen import GRID_PHOTO_PATH
from Screens.AuthenticationScreens.pixels_screen import PIXEL_PHOTO_PATH
from Utils.tkinter_utils import destroy_screens, add_screen


class CubeScreen(IAuthScreen):
    LENGTH = 800

    def __init__(self, auth):
        super().__init__(auth)

        self.cube_screen = None

        self._password = ""
        self.current = None
        self.drawing = None
        self.photo = None

    @property
    def password(self):
        return self._password

    @property
    def screen(self):
        return self.cube_screen

    def _create_canvas(self):
        self.drawing = Canvas(self.cube_screen, width=750, height=473, bg='white')
        self.drawing.pack()
        self.photo = ImageTk.PhotoImage(Image.open(PIXEL_PHOTO_PATH + "\\" + "switzerland.jpg"))
        self.drawing.create_image(0, 0, image=self.photo, anchor=NW)

        self.drawing.bind("<Motion>", self._motion)
        self.drawing.bind("<ButtonPress-1>", self._mouse_down)

    def _create(self, screen, button_clear_command, button_finished):
        self.cube_screen = add_screen(screen, "Cube image part", "750x600")

        self._create_canvas()

        Label(self.cube_screen, text="").pack()
        Button(self.cube_screen, text="Clear", width=20, height=1,
               command=button_clear_command).pack()

    def handle_register(self, register_screen):
        button_finish_command = lambda: destroy_screens(self.cube_screen)

        self._create(register_screen, self._reset_all_lines, button_finish_command)

    def handle_login(self, login_screen, username, email):
        self.lines = []
        self._reset_all_lines()
        button_finish_command = lambda: self._verify(login_screen, username, email)

        self._create(login_screen, self._reset_all_lines, button_finish_command)

    def _verify(self, login_screen, username, email):
        if self.authenticator.verify_lines_password(username, self._password):
            login.login_success = True
            self._reset_all_lines()
            destroy_screens(self.cube_screen)
        else:
            self._reset_all_lines()
            self._login_failed(login_screen, username, email)

    def _mouse_down(self, event):
        event.widget.focus_set()  # so escape key will work

        if self.current is None:
            x0 = event.x
            y0 = event.y
            self.current = event.widget.create_rectangle(x0, y0, event.x, event.y)

        else:
            coords = event.widget.coords(self.current)
            x0 = coords[2]
            y0 = coords[3]

            self._password = coords
            destroy_screens(self.cube_screen)

    def _motion(self, event):
        if self.current:
            # modify the current line by changing the end coordinates
            # to be the current mouse position
            coords = event.widget.coords(self.current)

            coords[2] = event.x
            coords[3] = event.y

            event.widget.coords(self.current, *coords)

    def _reset_all_lines(self):
        self.drawing.delete(self.current)
        self.current = None
        self._password = ""
