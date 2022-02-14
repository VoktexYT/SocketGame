# import...
import pygame
import json
from game import Game, OnlinePlayer

# init instance
pygame.init()
game = Game()

# create screen
screen = pygame.display.set_mode(game.screenSize)
pygame.display.set_caption(game.screenTitle)
coloringScreen = lambda: screen.fill(game.color['blue:dark'])
pygame.display.flip()
loop = True

# Call server: new player -> server give rule (player position, player id)
game_rule = json.loads(game.CallEvent(game.allEvent[0], game.player.avatar))
number_player_online = len(game_rule) - 1
game_rule_online = {}
for i in game_rule:
    if i != game.player.avatar['id']:
        game_rule_online[i] = game_rule[i]
id_player_online = [x for x in game_rule_online]

after_game_rule = game_rule

# create the other player if there are
if game_rule_online != 0:
    online_player = OnlinePlayer(number_player_online)

# Game loop
while game.screenRun:
    game_rule = json.loads(game.CallEvent(game.allEvent[3]))
    number_player_online = len(game_rule) - 1
    game_rule_online = {}
    for i in game_rule:
        if i != game.player.avatar['id']:
            game_rule_online[i] = game_rule[i]

    if number_player_online != len(after_game_rule)-1:
        if number_player_online > len(after_game_rule)-1:
            online_player = OnlinePlayer(number_player_online)
        after_game_rule = game_rule

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
        pygame.K_RIGHT: game.player.moveRight,
    }

    for i in game.player.btnPressed:
        if game.player.btnPressed.get(i) and i in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            eventKeysPressed.get(i)()
            game.CallEvent(game.allEvent[1], game.player.avatar)
            break
    else:
        pass

    # display all player if not alone or one player if alone
    if number_player_online != 0:
        for i in range(number_player_online):
            print(online_player.players[f'player{i}'].rect)
            screen.blit(online_player.players[f'player{i}'].image, online_player.players[f'player{i}'].rect)

    screen.blit(game.player.image, game.player.rect)
    pygame.display.update()

pygame.quit()
print('ends game')
game.CallEvent(game.allEvent[2], game.player.avatar)