from PIL import ImageTk, Image
import tkinter as tk

starting_positions = ((0,3),(0,6),(3,0),(3,9),(6,0),(6,9),(9,3),(9,6))
step_moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
horizontal = ("10","9","8","7","6","5","4","3","2","1")
vertical = ("a","b","c","d","e","f","g","h","i","j")

cwd = "C:/Users/Mat/Documents/GitHub/Amazon/Amazons2/sprites/"

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
        game.check_click(self.piece, self.coor)

    def update_sprite(self):
        self.path = f"{cwd}{self.tile_color}_{self.piece}.png"
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

    def check_click(self, piece, coor):
        #pick white amazon
        if self.state == 0 and piece == "white_amazon":
            no_move = self.possible_moves(coor)
            if no_move:
                return
            self.selected_amazon_coor = coor
            self.state += 1
            return

        #pick move tile
        if self.state == 1 and piece == "selection":
            self.clear_possible_moves()
            self.move_amazon(self.selected_amazon_coor,coor)
            self.possible_moves(coor)
            self.state += 1
            return

        #pick arrow tile
        if self.state == 2 and piece == "selection":
            self.clear_possible_moves()
            self.shoot_arrow(coor)
            self.state += 1
            return

        #pick black amazon
        if self.state == 3 and piece == "black_amazon":
            no_move = self.possible_moves(coor)
            if no_move:
                return
            self.selected_amazon_coor = coor
            self.state += 1
            return

        #pick move tile
        if self.state == 4 and piece == "selection":
            self.clear_possible_moves()
            self.move_amazon(self.selected_amazon_coor,coor)
            self.possible_moves(coor)
            self.state += 1
            return

        #pick arrow tile
        if self.state == 5 and piece == "selection":
            self.clear_possible_moves()
            self.shoot_arrow(coor)
            self.state = 0
            return

    def check_player_moves(self):
        player_moves = []
        for row in self.tiles:
            for tile in row:
                if tile.piece == self.player+"_amazon":
                    player_moves.append(self.check_amazon_moves(tile))

    def check_amazon_moves(self,coor):
        i,j = coor
        no_move = True
        for step_move in step_moves:
            for m in range(1,10):
                x = i + step_move[0]*m
                y = j + step_move[1]*m
                if x < 0 or x > 9 or y < 0 or y > 9:
                    break
                if self.tiles[y][x].piece == "empty":
                    self.tiles[y][x].piece = "selection"
                    self.tiles[y][x].update_sprite()
                    no_move = False
                else:
                    break
        return no_move

    def clear_possible_moves(self):
        for row in self.tiles:
            for tile in row:
                if tile.piece == "selection":
                    tile.piece = "empty"
                    tile.update_sprite()

    def move_amazon(self,selected_amazon_coor,coor):
        i,j = selected_amazon_coor
        temp = self.tiles[j][i].piece
        self.tiles[j][i].piece = "empty"
        self.tiles[j][i].update_sprite()
        i,j = coor
        self.tiles[j][i].piece = temp
        self.tiles[j][i].update_sprite()

    def shoot_arrow(self,coor):
        i,j = coor
        self.tiles[j][i].piece = "arrow"
        self.tiles[j][i].update_sprite()

    def reset_board(self):
        pass

root = tk.Tk()
board_size=10
game = Board(root,board_size)
root.mainloop()
