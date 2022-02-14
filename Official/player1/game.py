import player
import socket
import json


class Game:
    def __init__(self):
        self.player = player.Player()

        self.screenSize = (800, 800)
        self.screenTitle = "Socket Game"
        self.screenRun = True

        self.color = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255)
        }

        self.allEvent = [
            # for client in game
            'players:new',
            'players:move',
            'players:death',

            # has the information for other player
            'get:players:position',
            'get:players:inGame',
            'get:players'
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

    def CallEvent(self, Event, param=None):
        if Event in self.allEvent:
            EventJSON = {'Event': Event}
            if param is not None:
                EventJSON.update(param)
            return self.CallSocket(json.dumps(EventJSON))
        else:
            raise SyntaxError
