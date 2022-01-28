import pygame
from game import Game

pygame.init()
game = Game()

# config screen
screen = pygame.display.set_mode(game.screenSize)
pygame.display.set_caption(game.screenTitle)
screen.fill(game.color['white'])

pygame.display.flip()


while game.screenRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.screenRun = False

pygame.quit()