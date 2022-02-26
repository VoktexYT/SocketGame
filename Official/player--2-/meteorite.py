import pygame


class Meteorite(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.meteoriteSize = (120, 200)
        self.image = pygame.image.load('img/commet.png')
        self.image = pygame.transform.scale(self.image, self.meteoriteSize)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.velocity = 3

    def deathPlayer(self):
        if self.game.checkCollision(self, self.game.all_players):
            return True