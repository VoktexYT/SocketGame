# import...
import pygame
import json
from game import Game, OnlinePlayer

# init instance
pygame.init()
game = Game()

# create and stylising game screen
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

# saved the after rule for comparison
after_game_rule = game_rule

# create the other player if there are
if game_rule_online != 0:
    online_player = OnlinePlayer(number_player_online)
    for i in range(number_player_online):
        online_player.players[f'player{i}'].avatar['id'] = id_player_online[i]

# Game loop
while game.screenRun:
    game_rule = json.loads(game.CallEvent(game.allEvent[3]))
    number_player_online = len(game_rule) - 1
    game_rule_online = {}
    commitPosition = tuple(map(int, game.CallEvent(game.allEvent[4]).split('.')))

    # fill game rule for all online player
    for i in game_rule:
        if i != game.player.avatar['id']:
            game_rule_online[i] = game_rule[i]

    # check if player connect or disconnect
    if number_player_online != len(after_game_rule)-1:
        if number_player_online > len(after_game_rule)-1:
            online_player = OnlinePlayer(number_player_online)
        after_game_rule = game_rule

    # update function
    coloringScreen()
    game.meteorite.rect.x = commitPosition[0]
    game.meteorite.rect.y = commitPosition[1]

    if game.meteorite.deathPlayer():
        game.screenRun = False

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
        for i, id_ in enumerate(game_rule_online):
            online_player.players[f'player{i}'].rect.x = game_rule_online[id_]['position'][0]
            online_player.players[f'player{i}'].rect.y = game_rule_online[id_]['position'][1]
            screen.blit(online_player.players[f'player{i}'].image, online_player.players[f'player{i}'].rect)

    # display local player, meteorite
    screen.blit(game.meteorite.image, game.meteorite.rect)
    screen.blit(game.player.image, game.player.rect)
    pygame.display.update()

# close all and call server for disconnect
pygame.quit()
game.CallEvent(game.allEvent[2], game.player.avatar)