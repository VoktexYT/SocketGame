# Import
import pygame.sprite

from player import Player
from meteorite import Meteorite
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
    def __init__(self, username):
        self.screenSize = (800, 800)
        self.screenTitle = f"Socket Game ({str(__file__).split('/')[-2]})"
        self.screenRun = True

        self.player = Player(username)
        self.meteorite = Meteorite(self)

        self.all_players = pygame.sprite.Group()
        self.all_players.add(self.player)

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
            'get:rule',
            'commit:move'
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

    # check if 2 or several entity collision
    def checkCollision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
