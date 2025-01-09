import os
from tkinter.filedialog import askopenfilename
import tkinter as tk

from threading import Thread

def load_from_path(path: str) -> list[tuple[int, int]] | None:
    """
    Reads file at "path" and returns a list with tuples of coordinates for each cell with format (x, y) or
    None if unable to load or format file at path.
    """

    try:
        if not os.path.exists(path):
            return None

        coords = []
        with open(path) as file:
            for coord in file:
                x, y = map(int, coord.strip().split(" "))
                coords.append((x, y))
        return coords
    
    except (FileNotFoundError, ValueError) as e: # borde inte få FileNotFound, men bara för att vara säker
        print("Invalid foramt or path.")
        return None


def __ask_open_file() -> list[tuple[int, int]] | None:
    """
    -- Private Function -- 
    Gives the user a "ask open file" dialog. This blocks the current thread.
    Returns a list with tuples of coordinates for each cell with format (x, y) or
    None if unable to load or format file at path.
    """
    root = tk.Tk()
    root.withdraw()
    path = askopenfilename()
    root.destroy()
    return load_from_path(path)


__open_file_dialogs = 0
def on_file_opened(callback):
    """
    Gives the user a "ask open file" dialog and exectues callback with a list
    of coordinates or None as argument. This executes in a new thread.
    """

    global __open_file_dialogs

    if __open_file_dialogs > 0:
        print("File dialog already opened!")
        return
    __open_file_dialogs += 1
    
    def __thread_wrapper(callback):
        """ Wraper function for thread """
        coords = __ask_open_file()
        callback(coords)
        global __open_file_dialogs
        __open_file_dialogs -= 1
    
    thread = Thread(target=__thread_wrapper, args=(callback,))
    thread.start()
