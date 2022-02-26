# Import
import pygame
import uuid
import random


# class PLayer for create avatar (id, position) and pygame sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.playerSize = (130, 130)
        self.btnPressed = {}
        self.velocity = 1

        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, self.playerSize)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 200)
        self.rect.y = random.randint(50, 200)

        self.id = str(uuid.uuid4())

        self.avatar = {
            "id": self.id,
            "position": [self.rect.x, self.rect.y]
        }

    def moveLeft(self):
        self.rect.x -= self.velocity
        self.avatar['position'][0] = self.rect.x

    def moveRight(self):
        self.rect.x += self.velocity
        self.avatar['position'][0] = self.rect.x

    def moveUp(self):
        self.rect.y -= self.velocity
        self.avatar['position'][1] = self.rect.y

    def moveDown(self):
        self.rect.y += self.velocity
        self.avatar['position'][1] = self.rect.y