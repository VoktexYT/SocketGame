import player


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
