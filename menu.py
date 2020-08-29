from PIL import ImageTk, Image
import tkinter as tk

# def start_game(board_size=10):
#     game = backend.Board(root,board_size)


# start_button = tk.Button(root, text="start", command=start_game)
# start_button.grid()

class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Game of the Amazons", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.singleplayer = tk.Button(self, text="Play singleplayer",
                            command=controller.display_board)
        self.singleplayer.pack()

        self.small_board = tk.Radiobutton(self, text="6x6", 
                                    variable=controller.board_size, value=6, 
                                    indicatoron=False, width=8)
        self.medium_board = tk.Radiobutton(self, text="8x8", 
                                    variable=controller.board_size, value=8, 
                                    indicatoron=False, width=8)
        self.big_board = tk.Radiobutton(self, text="10x10", 
                                    variable=controller.board_size, value=10, 
                                    indicatoron=False, width=8)
        self.small_board.pack(side="left")
        self.medium_board.pack(side="left")
        self.big_board.pack(side="left")

        self.ai = tk.Radiobutton(self, text="AI", 
                                    variable=controller.ai, value=True, 
                                    indicatoron=False, width=8)

if __name__ == "__main__":
    from amazon import Amazon
    a = Amazon()
    a.mainloop()