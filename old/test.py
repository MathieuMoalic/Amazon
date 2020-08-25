import pygame
import numpy as np

pygame.init()

win = pygame.display.set_mode((450,450))
pygame.display.set_caption("Amazons")

img_blackArrow = pygame.image.load('sprites/BlackArrow.png')
img_whiteArrow = pygame.image.load('sprites/WhiteArrow.png')
img_blackQueen = pygame.image.load('sprites/BlackQueen.png')
img_whiteQueen = pygame.image.load('sprites/WhiteQueen.png')
img_blackSquare = pygame.image.load('sprites/BlackSquare.png')
img_whiteSquare = pygame.image.load('sprites/WhiteSquare.png')

board = np.zeros((10,10))########
boardSprites = pygame.sprite.Group()

class cell(pygame.sprite.Sprite):
	def __init__(self, img,x,y):
       # Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)

		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

a = cell(img_blackArrow,90,90)
boardSprites.add(a)

for i in board:
	for j in board[i]:
		square = board[i][j]
		if square == 1:
			boardSprites.add(a)

boardSprites.draw(win)

def draw():
	boardSprites.draw(win)
	pygame.display.update()

run = True
while run:
	pygame.time.Clock().tick(10)

	keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT or keys[pygame.K_SPACE]:
			run = False
	draw()