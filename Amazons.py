import numpy as np
import time

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
		self.pieces = {1:'White', 0: '-', -1:'Black', 2:'Arrow'}

		self.cleanBoard = np.zeros((self.boardSize,self.boardSize), dtype=np.int)
		self.board = self.startingBoard()
		self.inputsB = []
		self.inputsW = []

	def reset(self):
		self.gameState = GameState(self.cleanBoard, 1)
		self.playerTurn = 1
		return self.gameState

	def startingBoard(self):
		b=self.cleanBoard
		if self.boardSize == 6:
			b[0][1]=b[0][4]=1
			b[5][1]=b[5][4]=-1
			return b
		if self.boardSize == 8:
			b[0][3]=b[2][0]=b[2][7]=1
			b[7][4]=b[5][0]=b[5][7]=-1
			return b
		if self.boardSize == 10:
			b[0][3]=b[0][6]=b[3][0]=b[3][9]=1
			b[9][3]=b[9][6]=b[6][0]=b[6][9]=-1
			return b

	def savingInputs(self):
		dictval = {-1:[1,0,0,0],0:[0,1,0,0],1:[0,0,1,0],2:[0,0,0,1]}
		self.logs = []
		
		for i in range(self.boardSize):
			for j in range(self.boardSize):
				log = dictval[self.board[i][j]]
				self.logs.append(log)

		if self.playerTurn == 1 :
			self.inputsW.append(self.logs)
		else:
			self.inputsB.append(self.logs)

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
					if  xMove >= 0 and xMove <= self.boardSize-1 and yMove >= 0 and yMove <= self.boardSize-1 :
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
			#queens = [[queenX,queenY],[[move1x, move1y],[etc]]]
		return allowed

	def isEndGame(self):
		queens = self.allowedActions()
		for queenMove in queens:
			if len(queenMove[1])!=0:
				return False
		return True

	def playTurn(self):
		#chooses a random queen to move
		queens = self.allowedActions()
		np.random.shuffle(queens)
		queen = queens[0]
		#choose a random move among those allowed
		np.random.shuffle(queen[1])
		move = queen[1][0]
		x,y = move[0],move[1]
		#moves the queen and modifies the board
		self.board[x][y]=self.playerTurn
		self.board[queen[0][0]][queen[0][1]]=0
		#saving the board
		self.savingInputs()
		#picks the same queen
		queenPos = [x,y]
		queens = self.allowedActions()
		for queen in queens:
			if queen[0]==queenPos:
				shoots=queen[1]
				np.random.shuffle(shoots)
				shoot = shoots[0]
				self.board[shoot[0]][shoot[1]]=2
		self.savingInputs()

	def play(self):
		run = True
		while run:
			if not(self.isEndGame()):
				self.playTurn()
				self.playerTurn=-self.playerTurn
			else:
				run = False
				winner = self.pieces[-self.playerTurn]
				if -self.playerTurn==1:
					return self.inputsB
				else:
					return self.inputsW
				#print(self.inputs)
				#print(self.board)
				#print(winner,"won")

def trainData(n):
	for i in range(n):
		train_data = Game(size="normal").play()
		train_data = reshapeData(train_data)
		np.save("train_data/"+str(i)+"{}".format(str(int(time.time()))), 
			train_data)

def reshapeData(data):
	a = []
	for board in data:
		b = []
		for tile in board:
			for i in tile:
				b.append(i)
		a.append(b)
	return np.array(a)

def main():
	trainData(3000)



if __name__ == "__main__":
    main()