import os
from tkinter.filedialog import askopenfilename
import tkinter as tk

from threading import Thread

def load_from_path(path: str):
    """
    Reads file at "path" and return a generator with tuples of coordinates for
    each cell with format (x, y)
    """

    try:
        if not os.path.exists(path):
            return None

        coords = []
        with open(path) as file:
            for coord in file:
                x, y = map(int, coord.strip().split(" "))
                # yield (x, y)
                coords.append((x, y))
        return coords
    
    except (FileNotFoundError, ValueError) as e: # borde inte få FileNotFound, men bara för att vara säker
        print("Invalid foramt or path.")
        return None


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


__open_file_dialogs = 0
def on_file_opened(callback):
    global __open_file_dialogs

    if __open_file_dialogs > 0:
        print("File dialog already opened!")
        return
    __open_file_dialogs += 1
    
    def __thread_wrapper(callback):
        coords = __ask_open_file()
        callback(coords)
        global __open_file_dialogs
        __open_file_dialogs -= 1
    
    thread = Thread(target=__thread_wrapper, args=(callback,))
    thread.start()
