import pygame


class Meteorite(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.meteoriteSize = (120, 200)
        self.image = pygame.image.load('img/commet.png')
        self.image = pygame.transform.scale(self.image, self.meteoriteSize)

        self.origin_image = self.image

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.velocity = 3
        self.angle = 0
        self.rightAnimation = True
        self.leftAnimation = False

    def deathPlayer(self):
        if self.game.checkCollision(self, self.game.all_players):
            return False

    def animation(self):
        if self.rightAnimation:
            self.angle -= 0.07
            if self.angle <= -2:
                self.rightAnimation = False
                self.leftAnimation = True
        elif self.leftAnimation:
            self.angle += 0.07
            if self.angle >= 2:
                self.rightAnimation = True
                self.leftAnimation = False

        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
