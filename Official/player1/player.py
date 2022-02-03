import pygame
import uuid


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.playerSize = (130, 130)
        self.btnPressed = {}
        self.velocity = 1

        self.image = pygame.image.load('/home/guertinu/CODE/Python/SocketGame/Official/Img/player.png')
        self.image = pygame.transform.scale(self.image, self.playerSize)

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200

        self.id = str(uuid.uuid4())

        self.avatar = {#3 Event (death, new, move)
            "Event": '',
            "id": self.id,
            "position": (self.rect.x, self.rect.y)
        }

    def moveLeft(self):
        self.rect.x -= self.velocity

    def moveRight(self):
        self.rect.x += self.velocity

    def moveUp(self):
        self.rect.y -= self.velocity

    def moveDown(self):
        self.rect.y += self.velocity
