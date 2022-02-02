# import...
import pygame
import socket
from game import Game
import json

# init instance
pygame.init()
game = Game()


# config server communication
def callSocket(msg: str):
    s = socket.socket()
    host = socket.gethostname()
    port = 10_000
    try:
        s.connect((host, port))
    except socket.error as e:
        print(str(e))
        exit()
    s.send(msg.encode())
    s.close()


# def getSocket():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     port = 10_001
#     host = socket.gethostname
#     s.bind((port, host))
#     msg = s.recv(1024)
#     print(msg)


# call server (for generate new player)
callSocket(json.dumps(game.player.avatar))

# config screen
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

    if game.player.btnPressed.get(pygame.K_UP):
        game.player.moveUp()
    elif game.player.btnPressed.get(pygame.K_DOWN):
        game.player.moveDown()
    elif game.player.btnPressed.get(pygame.K_LEFT):
        game.player.moveLeft()
    elif game.player.btnPressed.get(pygame.K_RIGHT):
        game.player.moveRight()

    screen.blit(game.player.image, game.player.rect)

    pygame.display.update()

pygame.quit()
print('ends game')

game.player.avatar['remove'] = True
callSocket(json.dumps(game.player.avatar))
#getSocket()