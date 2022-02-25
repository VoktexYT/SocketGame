# Import
from player import Player
import socket
import json


# create dict with all online player
class OnlinePlayer:
    def __init__(self, nbrPlayer):
        self.players = {}
        for i in range(nbrPlayer):
            self.players[f'player{i}'] = Player()


# this is all configuration for the game
class Game:
    def __init__(self):
        self.player = Player()

        self.screenSize = (800, 800)
        self.screenTitle = f"Socket Game ({str(__file__).split('/')[-2]})"
        self.screenRun = True

        self.color = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),

            'blue:dark': (2, 48, 71)
        }

        self.allEvent = [
            # for client in game
            'players:new',
            'players:move',
            'players:death',

            # has the information for other player
            'get:rule'
        ]

        self.socket_host = socket.gethostname()
        self.socket_port = 10_000

    # config server communication
    def CallSocket(self, msg: str):
        s = socket.socket()
        try:
            s.connect((self.socket_host, self.socket_port))
        except socket.error as e:
            print(str(e))
            exit()
        s.send(msg.encode())
        data = s.recv(1024)
        s.close()
        return data.decode()

    # call "CallSocket" function with param
    def CallEvent(self, Event, param=None):
        if Event in self.allEvent:
            EventJSON = {'Event': Event}
            if param is not None:
                EventJSON.update(param)
            return self.CallSocket(json.dumps(EventJSON))
        else:
            raise SyntaxError
