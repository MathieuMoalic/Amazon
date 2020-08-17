import socket
import pickle

#network aspect of the client
#https://docs.python.org/3/library/socket.html
class Network:
    def __init__(self):
        #hamachi IPv4 = 25.73.105.10
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #CHANGE IF HOST IS NOT ON THE SAME PC
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            print("client connecting to server ...")
            self.client.connect(self.addr)
            #receive a response: the player number
            player = pickle.loads(self.client.recv(2048))
            return player 
        except:
            pass

    def getBoard(self):
        try:
            print("client receiving the new board...")
            board = pickle.loads(self.client.recv(2048*256))
            print("client received the new board")
            return board
        except socket.error as e:
            print("client couldn't receive the new board")
            print(e)

    def sendMpos(self,mpos):
        try:
            print("client sending mpos...")
            self.client.send(pickle.dumps(mpos))
            print("client send mpos")
        except socket.error as e:
            print("client couldn't send mpos")
            print(e)


