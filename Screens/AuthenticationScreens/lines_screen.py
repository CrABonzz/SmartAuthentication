from tkinter import Label, END, StringVar, Button, Canvas

from Screens import login
from Screens.AuthenticationScreens.authentication_screen import AuthScreen
from Utils.tkinter_utils import destroy_screens, add_screen


class LinesScreen(AuthScreen):
    LENGTH = 500

    WIDTH = 4

    def __init__(self, auth):
        super().__init__(auth)

        self.lines_screen = None

        self._password = ""
        self.current = None
        self.lines = []
        self.drawing = None

    @property
    def password(self):
        return self._password

    @property
    def screen(self):
        return self.lines_screen

    def _create_canvas(self):
        self.drawing = Canvas(self.lines_screen, width=self.LENGTH, height=self.LENGTH, bg='white')
        self.drawing.pack()
        self._draw_grid()

        # Set the user's mouse callbacks
        self.drawing.bind("<Motion>", self._motion)
        self.drawing.bind("<ButtonPress-1>", self._mouse_down)

    def _create(self, screen, button_clear_command, button_finished):
        self.lines_screen = add_screen(screen, "Draw lines", "600x600")

        self._create_canvas()

        Label(self.lines_screen, text="").pack()
        Button(self.lines_screen, text="Clear all", width=20, height=1,
               command=button_clear_command).pack()

        Label(self.lines_screen, text="").pack()
        Button(self.lines_screen, text="Finished", width=20, height=1,
               command=button_finished).pack()
        Label(self.lines_screen, text="").pack()

    def handle_register(self, register_screen):
        self._reset_all_lines()
        button_finish_command = lambda: destroy_screens(self.lines_screen)

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
            destroy_screens(self.lines_screen)
        else:
            self._reset_all_lines()
            self._login_failed(login_screen, username, email)

    def _draw_grid(self, line_distance=LENGTH // WIDTH):
        for x in range(line_distance, self.LENGTH, line_distance):
            self.drawing.create_line(x, 0, x, self.LENGTH, fill="#d3d3d3")

        for y in range(line_distance, self.LENGTH, line_distance):
            self.drawing.create_line(0, y, self.LENGTH, y, fill="#d3d3d3")

    def _reset_current_line(self, event):
        self.current = None

    def _get_cube_index(self, event):
        return int(event.y * self.WIDTH / self.LENGTH) * 4 + int(event.x * self.WIDTH / self.LENGTH)

    def _mouse_down(self, event):
        """ QT callback on pressing mouse """
        event.widget.focus_set()  # so escape key will work

        if self.current is None:
            x0 = event.x
            y0 = event.y
        else:
            coords = event.widget.coords(self.current)
            x0 = coords[2]
            y0 = coords[3]

        self.current = event.widget.create_line(x0, y0, event.x, event.y)
        self.lines += [self.current]
        self._password += str(self._get_cube_index(event)) + ", "

    def _motion(self, event):
        """ QT callback for mouse moving """
        if self.current:
            # modify the current line by changing the end coordinates
            # to be the current mouse position
            coords = event.widget.coords(self.current)
            coords[2] = event.x
            coords[3] = event.y

            event.widget.coords(self.current, *coords)

    def _reset_all_lines(self):
        self.current = None

        if self.drawing is not None:
            for line in self.lines:
                self.drawing.delete(line)

        self._password = ""
        self.lines = []

