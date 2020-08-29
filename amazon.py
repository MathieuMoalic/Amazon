from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font as tkfont

from game import Board
from menu import Menu

class Amazon(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Amazon")
        self.board_size = tk.IntVar(value=10)
        self.ai = tk.BooleanVar(value=False)
        self.container = tk.Frame(self)
        self.container.grid()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.current_frame = Menu(parent=self.container, controller=self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def display_menu(self):
        self.current_frame.destroy()
        self.current_frame = Menu(parent=self.container, controller=self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def display_board(self):
        self.current_frame.destroy()
        self.current_frame = Board(parent=self.container, controller=self, board_size=self.board_size.get(), ai=self.ai.get())
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def reset_game(self):
        frame =  Board(parent=self.container, controller=self)
        self.frames[Board.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

# frm.destroy()

if __name__ == "__main__":
    a = Amazon()
    a.mainloop()