import numpy as np
import pygame


class Game:
	def __init__(self,size="tiny"):
		self.name = 'Amazons'

		if size == "tiny":
			self.boardSize = 6
		elif size == "small":
			self.boardSize = 8
		else:
			self.boardSize = 10

		self.playerTurn = 1
		self.pieces = {1:'White', 0: '-', -1:'Black', 2:'Arrow', 3:'Red'}

		self.cleanBoard = np.zeros((self.boardSize,self.boardSize), dtype=np.int)
		self.board = self.startingBoard()

		self.gui = GUI(self.board)
		self.playing = True

	def reset(self):
		self.board = self.startingBoard()
		self.playerTurn = 1

	def startingBoard(self):
		b = self.cleanBoard
		if self.boardSize == 6:
			b[1][0] = b[1][5] = -1
			b[4][0] = b[4][5] = 1
			return b
		if self.boardSize == 8:
			b[0][3] = b[2][0] = b[2][7] = -1
			b[7][4] = b[5][0] = b[5][7] = 1
			return b
		if self.boardSize == 10:
			b[0][3] = b[0][6] = b[3][0] = b[3][9] = -1
			b[9][3] = b[9][6] = b[6][0] = b[6][9] = 1
			return b

	def allowedActions(self):
		allowed = []
		moves = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
		arrayPos_x,arrayPos_y = np.where(self.board == self.playerTurn)

		#iter over the number of queens
		for iter in range(len(arrayPos_x)):
			# queen position
			queenMove = []
			x = arrayPos_x[iter]
			y = arrayPos_y[iter]
			#iter over the possible directions
			for move in moves:
				xMove = x + move[0]
				yMove = y + move[1]
				run = True
				while run:
					if  xMove >= 0 and xMove <= self.boardSize - 1 and yMove >= 0 and yMove <= self.boardSize - 1 :
						if self.board[xMove][yMove] == 0 :
							queenMove.append([xMove,yMove])
							xMove += move[0]
							yMove += move[1]
						else:
							run = False
					else:
						run = False
			if len(queenMove) != 0:
				allowed.append([[x,y],queenMove])
		return allowed

	def isEndGame(self):
		queens = self.allowedActions()
		for queenMove in queens:
			if len(queenMove[1]) != 0:
				return False
		return True

	def AITurn(self):
		#chooses a random queen to move
		queens = self.allowedActions()
		np.random.shuffle(queens)
		if len(queens)!=0:
			queen = queens[0]
		else:
			return
		#choose a random move among those allowed
		np.random.shuffle(queen[1])
		move = queen[1][0]
		x,y = move[0],move[1]
		#moves the queen and modifies the board
		self.board[x][y] = self.playerTurn
		self.board[queen[0][0]][queen[0][1]] = 0
		#picks the same queen
		queenPos = [x,y]
		queens = self.allowedActions()
		for queen in queens:
			if queen[0] == queenPos:
				shoots = queen[1]
				np.random.shuffle(shoots)
				shoot = shoots[0]
				self.board[shoot[0]][shoot[1]] = 2
		self.playerTurn = -self.playerTurn

	def humanTurn(self):
		self.stage = 1
		self.queenPos = [0,0]
		run = True
		while run and self.playing:
			pygame.time.Clock().tick(10)
			events = pygame.event.get()
			self.quit(events)
			self.gui.draw()

			if self.stage == 1:
				self.pickQueen(events)
			if self.stage == 2:
				self.pickRedTile(events)
			if self.stage == 3:
				run = self.pickRedTileArrow(events)
		self.playerTurn = -self.playerTurn

	def showPossibility(self,tilePos):
		possibleMove = self.allowedActions()
		for move in possibleMove:
			#if it's our queen
			if move[0]==tilePos:
				for red in move[1]:
					self.board[red[0],red[1]]=3

	def clearRedTiles(self):
		for j in range(len(self.board)):
			for i in range(len(self.board[j])):
				if self.board[i][j] == 3:
					self.board[i][j] = 0

	def pickQueen(self,events):
		queens = self.gui.listval(self.playerTurn)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and self.stage==1:
					for queen in queens:
						if queen.rect.collidepoint(pygame.mouse.get_pos()) and self.stage==1:
							self.showPossibility([queen.pos[1],queen.pos[0]])
							self.queenPos = queen.pos
							self.stage = 2
							break

	def pickRedTile(self,events):
		redTiles = self.gui.listval(3)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and self.stage==2:
					for redTile in redTiles:
						if redTile.rect.collidepoint(pygame.mouse.get_pos()) and self.stage==2:
							self.board[self.queenPos[1],self.queenPos[0]]=0
							self.board[redTile.pos[1],redTile.pos[0]]=self.playerTurn
							self.queenPos = [redTile.pos[1],redTile.pos[0]]
							self.clearRedTiles()
							self.showPossibility(self.queenPos)
							self.stage = 3
							break

	def pickRedTileArrow(self,events):
		self.gui = GUI(self.board)
		self.gui.draw()
		redTiles = self.gui.listval(3)

		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and self.stage==3:
				for redTile in redTiles:
					if redTile.rect.collidepoint(pygame.mouse.get_pos()) and self.stage==3:
						self.board[redTile.pos[1],redTile.pos[0]]=2
						self.clearRedTiles()
						self.stage == 4
						return False
		return True

	def quit(self,events):
		for event in events:
			#quit game ?
			keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
				print("quitting")
				self.playing = False

	def play(self,WhiteAI,BlackAI):
		while not(self.isEndGame()) and self.playing:
			pygame.time.Clock().tick(10)
			events = pygame.event.get()
			self.quit(events)
			self.gui.draw()
			
			if self.playerTurn == 1:
				if WhiteAI:
					self.AITurn()
				else:
					self.humanTurn()

			if self.playerTurn == -1:
				if BlackAI:
					self.AITurn()
				else:
					self.humanTurn()

		winner = self.pieces[-self.playerTurn]
		print(winner,"won")
		self.reset()
		pygame.quit()

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
		self.window = pygame.display.set_mode((len(board)*45,len(board)*45))
		pygame.display.set_caption("Amazons")
		self.boardSprites = pygame.sprite.Group()
		self.board = board
		pygame.init()

		#dark tiles
		self.dark_arrow = pygame.image.load('sprites/dark/arrow.png')
		self.dark_bqueen = pygame.image.load('sprites/dark/bqueen.png')
		self.dark_square = pygame.image.load('sprites/dark/square.png')
		self.dark_wqueen = pygame.image.load('sprites/dark/wqueen.png')
		self.dark_red = pygame.image.load('sprites/dark/red.png')
		#clear tiles
		self.clear_arrow = pygame.image.load('sprites/clear/arrow.png')
		self.clear_bqueen = pygame.image.load('sprites/clear/bqueen.png')
		self.clear_square = pygame.image.load('sprites/clear/square.png')
		self.clear_wqueen = pygame.image.load('sprites/clear/wqueen.png')
		self.clear_red = pygame.image.load('sprites/clear/red.png')		

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

if __name__ == "__main__":
    Game(size="normal").play(False,True)
