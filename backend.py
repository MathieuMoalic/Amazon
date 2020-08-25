from PIL import ImageTk, Image
import tkinter as tk

starting_positions = ((0,3),(0,6),(3,0),(3,9),(6,0),(6,9),(9,3),(9,6))
step_moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
horizontal = ("10","9","8","7","6","5","4","3","2","1")
vertical = ("a","b","c","d","e","f","g","h","i","j")

class Tile:
    def __init__(self,board,i,j):
        self.coor = (i,j)
        self.pos = vertical[j]+horizontal[i]

        if (i+j)%2:
            self.tile_color = "dark"
        else:
            self.tile_color = "light"

        if self.coor in starting_positions:
            if i > 5:
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
        game.check_click(self)

    def change_piece(self,new_piece):
        self.piece = new_piece
        self.update_sprite()

    def update_sprite(self):
        self.path = f"sprites/{self.tile_color}_{self.piece}.png"
        self.image = ImageTk.PhotoImage(Image.open(self.path))
        self.cell.config(image = self.image)

class Board:
    def __init__(self,root,board_size):
        
        board = tk.Frame(root, bg="#a6bdbb", bd=15)
        board.grid()

        for i,letter in enumerate(vertical):
            a = tk.Label(board, bd=0, bg="#a6bdbb", text=letter, font=("Helvetica", 12), width=3, height=2)
            a.grid(row=0, column=i+1)
        for j,number in enumerate(horizontal):
            a = tk.Label(board, bd=-2, bg="#a6bdbb", text=number, font=("Helvetica", 12), width=3, height=2)
            a.grid(row=j+1, column=0)

        restart_button = tk.Button(board, text="restart", command=self.reset_board)
        restart_button.grid(row=board_size+2, column=1)

        self.tiles = [[Tile(board,i,j) for i in range(board_size)] for j in range(board_size)]

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
                if x < 0 or x > 9 or y < 0 or y > 9:
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
        pass

root = tk.Tk()
board_size=10
game = Board(root,board_size)
root.mainloop()
