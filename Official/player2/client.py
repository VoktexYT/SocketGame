# import...
import pygame
from game import Game

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

    # for move player (screen, socket)
    eventKeysPressed = {
        pygame.K_UP: game.player.moveUp,
        pygame.K_DOWN: game.player.moveDown,
        pygame.K_LEFT: game.player.moveLeft,
        pygame.K_RIGHT: game.player.moveRight
    }

    for i in game.player.btnPressed:
        if game.player.btnPressed.get(i) and i in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            eventKeysPressed.get(i)()
            game.CallEvent(game.allEvent[1], game.player.avatar)
            break
    else:
        pass

    # call server for number player
    nbrPlayer = len(game.CallEvent('get:players:id').split(':'))

    for i in range(nbrPlayer):
        screen.blit(game.player.image, game.player.rect)
        pygame.display.update()

pygame.quit()
print('ends game')
game.CallEvent(game.allEvent[2], game.player.avatar)