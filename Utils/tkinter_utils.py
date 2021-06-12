from tkinter import Label, Entry, Toplevel, Button, BooleanVar, Checkbutton, LEFT


def add_entry(screen, text, variable):
    label = Label(screen, text=text)
    label.pack()

    entry = Entry(screen, textvariable=variable)
    entry.pack()

    return entry


def add_screen(top_screen, title, size):
    screen = Toplevel(top_screen)
    screen.title(title)
    screen.geometry(size)

    return screen


def destroy_screens(*screens):
    for screen in screens:
        screen.destroy()


def info_screen(top_screen, title, size, label_text=None):
    screen = add_screen(top_screen, title, size)

    if label_text is None:
        label_text = title
    Label(screen, text=label_text).pack()
    Button(screen, text="Okay", command=lambda: destroy_screens(screen)).pack()

    return screen

def auth_method_checkbox(screen, text):
    auth_method = BooleanVar()
    check_button = Checkbutton(screen, text=text, variable=auth_method, onvalue=True, offvalue=False)
    check_button.pack(side=LEFT)

    return auth_method