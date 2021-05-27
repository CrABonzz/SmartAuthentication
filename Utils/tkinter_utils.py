from tkinter import Label, Entry, Toplevel


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