# import...
import pygame
from game import Game, OnlinePlayer

# init instance
pygame.init()
game = Game()

# call server (for generate new player) and (get information all player)
allPlayerId = game.CallEvent('get:players:id')
allPlayerPosition = game.CallEvent('get:players:position')
alonePlayer = False

if '204' not in [allPlayerId, allPlayerPosition]: # check there are one player or more online
    nbrPlayer = len(allPlayerId)
    onlinePlayer = OnlinePlayer(nbrPlayer)
    for i in onlinePlayer.players:
        eachPlayer = onlinePlayer.players.get(f'player{i}')
        selfId = eachPlayer.avatar['id']
        eachPlayer.rect = allPlayerPosition[selfId]
else:
    alonePlayer = True

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

    # display all player if not alone or one player if alone
    if not alonePlayer:
        for idPlayer in allPlayerId:
            screen.blit(onlinePlayer.players[idPlayer].image, onlinePlayer.players[idPlayer].image)

    screen.blit(game.player.image, game.player.rect)
    pygame.display.update()

pygame.quit()
print('ends game')
game.CallEvent(game.allEvent[2], game.player.avatar)