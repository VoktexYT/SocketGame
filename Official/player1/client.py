import pygame
import socket
from game import Game


# config server communication
def callSocket(msg: str):
    s = socket.socket()
    host = socket.gethostname()
    port = 10_000
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    c.sendall(msg.encode())
    c.close()


callSocket("New Player")

pygame.init()
game = Game()

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

    screen.blit(game.player.image, game.player.rect)

    pygame.display.update()

pygame.quit()