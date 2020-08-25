import socket
from _thread import *
import pickle
from Amazons_GUI import Game
import numpy as np

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#the client sends the mouse pos on left click
#the server sends back the board

#initialisation
# conn = conn is a new socket object usable to send and receive data on the
#connection
# addr = (IP,port) address is the address bound to the socket on the other
#end of the connection

#player = 1 or -1 (white or black)




def sendBoard(board):
    try:
        print("server sending the new board")
        conn1.send(pickle.dumps(board,protocol=-2))
        conn2.send(pickle.dumps(board,protocol=-2))
        print("server sent the new board")
    except socket.error as e:
        print("server couldnt send the new board")
        print(e)

def getMpos(conn):
    try:
        print("server receiving mpos...")
        mpos = pickle.loads(conn.recv(2048*2))
        print("server received mpos")
        return mpos
    except socket.error as e:
        print("server couldn't receive mpos")
        print(e)

def playing(conn,player):
    #each player has one of these running
    conn.send(pickle.dumps(game.board))
    run = True
    #white play first
    while run:
        sendBoard(game.board)
        if game.playerTurn == player:
            print('player',player,'is choosing the queen')
            mpos = getMpos(conn1)
            game.checkClick(mpos,game.board)

            print('player',player,'is moving the queen')
            mpos = getMpos(conn1)
            game.checkClick(mpos,game.board)

            print('player',player,'is shooting the arrow')
            mpos = getMpos(conn1)
            game.checkClick(mpos,game.board)
            #run = game.isEndGame()
            game.playerTurn *= -1

    print("Lost connection")
    isGamePlaying = False

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

game=Game(size="tiny")

conn1, addr1 = s.accept()
print("First player connected from:", addr1)

conn2, addr2 = s.accept()
print("Second player connected from:", addr2)

start_new_thread(playing, (conn1, 1))
start_new_thread(playing, (conn2, -1))

conn1.send(pickle.dumps(1))
conn2.send(pickle.dumps(-1))
print("Games started")

#to end process
# ctrl + break
#netstat -ano
#taskkill /F /PID port