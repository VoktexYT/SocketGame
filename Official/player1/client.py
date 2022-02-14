# import...
import pygame
from game import Game
import json

# init instance
pygame.init()
game = Game()

# call server (for generate new player)
game.CallEvent(game.allEvent[0], game.player.avatar)

# config pygame screen
screen = pygame.display.set_mode(game.screenSize)
pygame.display.set_caption(game.screenTitle)
coloringScreen = lambda: screen.fill(game.color['white'])
pygame.display.flip()
loop = True

while game.screenRun:
    coloringScreen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.screenRun = False
        elif event.type == pygame.KEYDOWN:
            game.player.btnPressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.player.btnPressed[event.key] = False

    if game.player.btnPressed.get(pygame.K_UP) or game.player.btnPressed.get(pygame.K_DOWN) or game.player.btnPressed.get(pygame.K_LEFT) or game.player.btnPressed.get(pygame.K_RIGHT):
        game.CallEvent(game.allEvent[1], json.dumps(game.player.avatar))

        if game.player.btnPressed.get(pygame.K_UP):
            game.player.moveUp()
        elif game.player.btnPressed.get(pygame.K_DOWN):
            game.player.moveDown()
        elif game.player.btnPressed.get(pygame.K_LEFT):
            game.player.moveLeft()
        elif game.player.btnPressed.get(pygame.K_RIGHT):
            game.player.moveRight()

    # call server for number player
    nbrPlayer = callSocket('GET-Player')
    screen.blit(game.player.image, game.player.rect)
    pygame.display.update()

pygame.quit()
print('ends game')

game.player.avatar['Event'] = 'death'
callSocket(json.dumps(game.player.avatar))