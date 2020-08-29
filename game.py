from PIL import ImageTk, Image
import tkinter as tk

starting_positions = {"10":((0,3),(0,6),(3,0),(3,9),(6,0),(6,9),(9,3),(9,6)), "8":((0,2),(7,7)), "6":((0,2),(5,5))}
step_moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
horizontal = ("10","9","8","7","6","5","4","3","2","1")
vertical = ("a","b","c","d","e","f","g","h","i","j")

class Tile(tk.Frame):
    def __init__(self, board, parent, controller, i, j, board_size):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # print(controller,parent)
        self.board = board
        self.coor = (i,j)
        self.pos = vertical[j]+horizontal[i]

        if (i+j)%2:
            self.tile_color = "dark"
        else:
            self.tile_color = "light"

        if self.coor in starting_positions[str(board_size)]:
            if i > board_size//2:
                self.piece = "white_amazon"
            else:
                self.piece = "black_amazon"
        else:
            self.piece = "empty"

        self.possible_moves = []

        self.cell = tk.Label(board, bd=-2)
        self.cell.grid(row=i+1, column=j+1)
        self.cell.bind("<Button-1>", self.on_click)

        self.update_sprite()

    def on_click(self,event):
        self.board.check_click(self)

    def change_piece(self,new_piece):
        self.piece = new_piece
        self.update_sprite()

    def update_sprite(self):
        self.path = f"sprites/{self.tile_color}_{self.piece}.png"
        self.image = ImageTk.PhotoImage(Image.open(self.path))
        self.cell.config(image = self.image)

class Board(tk.Frame):
    def __init__(self, parent, controller, board_size, ai):
        b = tk.Frame.__init__(self, parent, bg="#a6bdbb")
        self.parent = parent
        self.controller = controller
        self.board_size = board_size
        self.ai = ai
        for i in range(board_size+5):
            for j in range(board_size+2):
                self.grid_columnconfigure(i, minsize=45, weight=1)
                self.grid_rowconfigure(j, minsize=45, weight=1)

        for i,letter in enumerate(vertical[:board_size]):
            a = tk.Label(self, bd=0, bg="#a6bdbb", text=letter, font=("Helvetica", 12))
            a.grid(row=0, column=i+1)
        for j,number in enumerate(horizontal[10-board_size:]):
            a = tk.Label(self, bd=-2, bg="#a6bdbb", text=number, font=("Helvetica", 12))
            a.grid(row=j+1, column=0)

        self.restart_button = tk.Button(self, text="Restart", font=("Helvetica", 12), command=self.reset_board)
        self.restart_button.grid(row=2, column=board_size+2, columnspan=2)

        self.menu_button = tk.Button(self, text="Menu", font=("Helvetica", 12), command=controller.display_menu )
        self.menu_button.grid(row=4, column=board_size+2, columnspan=2)

        self.tiles = [[Tile(self, parent, controller,i,j,board_size) for i in range(board_size)] for j in range(board_size)]

        self.state = 0
        self.player = "white"
        self.check_player_moves()

    def check_click(self, tile):
        #pick white amazon
        if self.state == 0 and tile.piece == "white_amazon":
            self.show_possible_moves(tile)
            self.selected_amazon = tile

            self.state += 1
            return

        #pick move tile
        if self.state == 1 and tile.piece == "possible":
            self.move_amazon(self.selected_amazon,tile)
            self.check_moves(tile)
            self.show_possible_moves(tile)

            self.state += 1
            return

        #pick arrow tile
        if self.state == 2 and tile.piece == "possible":
            self.shoot_arrow(tile)

            self.state += 1
            self.player = "black"
            self.check_player_moves()
            return

        #pick black amazon
        if self.state == 3 and tile.piece == "black_amazon":
            self.show_possible_moves(tile)
            self.selected_amazon = tile

            self.state += 1
            return

        #pick move tile
        if self.state == 4 and tile.piece == "possible":
            self.move_amazon(self.selected_amazon,tile)
            self.check_moves(tile)
            self.show_possible_moves(tile)

            self.state += 1
            return

        #pick arrow tile
        if self.state == 5 and tile.piece == "possible":
            self.shoot_arrow(tile)

            self.state = 0
            self.player = "white"
            self.check_player_moves()
            return

    def check_player_moves(self):
        player_moves = [self.player]
        for row in self.tiles:
            for tile in row:
                if tile.piece == self.player+"_amazon":
                    moved = self.check_moves(tile)
                    player_moves.append(moved)
                    # print(f"{tile.pos=} {tile.piece} {moved=}")
        # print(player_moves)
        if True not in player_moves:
            print(f"{self.player} loses")

    def check_moves(self,tile):
        i,j = tile.coor
        moved = False
        for step_move in step_moves:
            for m in range(1,10):
                x = i + step_move[0]*m
                y = j + step_move[1]*m
                if x < 0 or x > self.board_size-1 or y < 0 or y > self.board_size-1:
                    break
                if self.tiles[y][x].piece == "empty":
                    tile.possible_moves.append((x,y))
                    moved = True
                else:
                    break
        # print(f"returning {moved=}")
        return moved

    def show_possible_moves(self,tile):
        for coor in tile.possible_moves:
            j,i = coor
            # if self.tiles[i][j].piece != "possible":
                # print(f"{self.state=} {self.tiles[i][j].piece=} {j=} {i=} {tile.pos=}")
            self.tiles[i][j].change_piece("possible")
            # tile.possible_moves = []

    def clear_possible_moves(self):
        for row in self.tiles:
            for tile in row:
                tile.possible_moves = []
                if tile.piece == "possible":
                    # print(f'cleared {tile.piece} in {tile.pos}')
                    tile.change_piece("empty")

    def move_amazon(self,previous_tile,new_tile):
        self.clear_possible_moves()
        temp = previous_tile.piece
        previous_tile.change_piece("empty")
        new_tile.change_piece(temp)
        # print("moved amazon")

    def shoot_arrow(self,tile):
        self.clear_possible_moves()
        tile.change_piece("arrow")
        # print("shot arrow")

    def reset_board(self):
        self.controller.reset_game()


if __name__ == "__main__":
    from amazon import Amazon
    a = Amazon()
    a.mainloop()