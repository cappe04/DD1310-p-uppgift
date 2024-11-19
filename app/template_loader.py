from tkinter.filedialog import askopenfilename
import tkinter as tk

from threading import Thread

def load_from_path(path: str):
    """
    Reads file at "path" and return a generator with tuples of coordinates for
    each cell with format (x, y)
    """
    with open(path) as file:
        for coord in file:
            x, y = map(int, coord.strip().split(" "))
            yield (x, y)

def __ask_open_file():
    """
    Gives the user a "ask open file" dialog. This blocks the current thread.
    Returns a generator with tuples of coordinates for each cell with format (x, y)
    """
    root = tk.Tk()
    root.withdraw()
    path = askopenfilename()
    root.destroy()
    return load_from_path(path)

def __thread_wrapper(callback):
    coords = __ask_open_file()
    callback(coords)

def on_file_opened(callback):
    thread = Thread(target=__thread_wrapper, args=(callback,))
    thread.start()
