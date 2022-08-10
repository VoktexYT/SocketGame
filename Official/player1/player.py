import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.playerSize = (130, 130)

        self.image = pygame.image.load('/home/---/CODE/Python/SocketGame/Official/Img/player.png')
        self.image = pygame.transform.scale(self.image, self.playerSize)

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200
