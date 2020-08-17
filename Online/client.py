import pygame
from network import Network
import pickle
import numpy as np


pygame.font.init()
pygame.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pieces = {1:'white', 0: '-', -1:'black', 2:'arrow'}
#window = pygame.display.set_mode((len(board)*45,len(board)*45))
pygame.display.set_caption("Game of the Amazons")
n=0

class Tile(pygame.sprite.Sprite):
    def __init__(self, img,x,y,val):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.imgWidth = 45
        self.image = img
        self.x = x
        self.y = y
        self.pos = [x,y]
        self.val = val
        self.rect = self.image.get_rect()
        self.rect.x = x*self.imgWidth
        self.rect.y = y*self.imgWidth

class GUI:
    def __init__(self,board):
        self.boardSprites = pygame.sprite.Group()
        self.board = board
        self.window = pygame.display.set_mode((len(board)*45,len(board)*45))
        path = "C:/rep/Games/Amazon/"
        #dark tiles
        self.dark_arrow = pygame.image.load(path + 'sprites/dark/arrow.png')
        self.dark_bqueen = pygame.image.load(path + 'sprites/dark/bqueen.png')
        self.dark_square = pygame.image.load(path + 'sprites/dark/square.png')
        self.dark_wqueen = pygame.image.load(path + 'sprites/dark/wqueen.png')
        self.dark_red = pygame.image.load(path + 'sprites/dark/red.png')
        #clear tiles
        self.clear_arrow = pygame.image.load(path + 'sprites/clear/arrow.png')
        self.clear_bqueen = pygame.image.load(path + 'sprites/clear/bqueen.png')
        self.clear_square = pygame.image.load(path + 'sprites/clear/square.png')
        self.clear_wqueen = pygame.image.load(path + 'sprites/clear/wqueen.png')
        self.clear_red = pygame.image.load(path + 'sprites/clear/red.png')     

    def listval(self,val):
        redTiles = []
        for tile in self.boardSprites:
            if tile.val == val:
                redTiles.append(tile)
        return redTiles

    def draw(self):
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if (i + j) % 2 == 0:
                    #if even => clear tiles
                    if self.board[i][j] == 1:
                        tile = Tile(self.clear_wqueen, j, i ,1)
                    if self.board[i][j] == 2:
                        tile = Tile(self.clear_arrow, j, i,2)
                    if self.board[i][j] == 0:
                        tile = Tile(self.clear_square, j, i,0)
                    if self.board[i][j] == -1:
                        tile = Tile(self.clear_bqueen, j, i,-1 )
                    if self.board[i][j] == 3:
                        tile = Tile(self.clear_red, j,i ,3)
                else:
                    if self.board[i][j] == 1:
                        tile = Tile(self.dark_wqueen, j, i,1)
                    if self.board[i][j] == 2:
                        tile = Tile(self.dark_arrow, j, i,2)
                    if self.board[i][j] == 0:
                        tile = Tile(self.dark_square, j, i,0)
                    if self.board[i][j] == -1:
                        tile = Tile(self.dark_bqueen, j, i ,-1)
                    if self.board[i][j] == 3:
                        tile = Tile(self.dark_red, j,i ,3)
                self.boardSprites.add(tile)
        self.boardSprites.draw(self.window)
        pygame.display.update()

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("calibri", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                #if click: connects
                n = Network()
                return n

def mpos():

    return pygame.mouse.get_pos()
def quit(events):
        for event in events:
            #quit game ?
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                print("quitting")
                return False
        return True
    
def play_screen():
    player = n.getPlayer() # 1 or -1
    board = n.getBoard()
    print("You are playing the", pieces[player],"Amazons.")
    #GUI(board).draw()

    playing = True
    while playing:
        pygame.time.Clock().tick(60)
        board = n.getBoard()
        GUI(board).draw()
        events = pygame.event.get()
        playing = quit(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("left click")
                    n.sendMpos(mpos())
                if event.button == 3:
                    print("right click")
                    #rechoose queen
                
                break

    



"""
def winner_screen():
    font = pygame.font.SysFont("calibri", 90)
        if game.winner() == 1:
            text = font.render("White won!", 1, (255,0,0))
        if game.winner() == -1:
            text = font.render("Black won!", 1, (255, 0, 0))
"""

def main():
    global n
    n = menu_screen()
    play_screen()
    winner_screen()
main()
