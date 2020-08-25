import tkinter as tk
from PIL import ImageTk, Image

import backend

# root = tk.Tk()

# path = r"C:\Users\Mat\Documents\GitHub\Amazon\sprites\clear\arrow.png"
# img = ImageTk.PhotoImage(Image.open(path))
# panel = tk.Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")

# root.mainloop()

class Display(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title('Amazons')
        # self.master.bind("<Key>", self.key_press)
        
        self.board = backend.board()

        self.board.mainloop()

        # self.update_idletasks()

amazons = Display()