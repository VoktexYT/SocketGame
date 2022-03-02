# import...
import pygame
import json
from game import Game, OnlinePlayer

# get information of player
username = input("Entry your username: ")

# init instance
pygame.init()
game = Game(username)

# create and stylising game screen
screen = pygame.display.set_mode(game.screenSize)
pygame.display.set_caption(game.screenTitle)
coloringScreen = lambda: screen.fill(game.color['blue:dark'])
pygame.display.flip()
loop = True

# Call server: new player -> server give rule (position, id, name)
game_rule = json.loads(game.CallEvent(game.allEvent[0], game.player.avatar))
number_player_online = len(game_rule) - 1
game_rule_online = {}

for i in game_rule:
    if i != game.player.avatar['id']:
        game_rule_online[i] = game_rule[i]

id_player_online = [x for x in game_rule_online]
name_player_online = [game_rule_online[x]['name'] for x in game_rule_online]

# saved the after rule for comparison
after_game_rule = game_rule


# update rule for online player
def onlinePlayer():
    global after_game_rule
    global online_player
    global name_player_online
    global id_player_online

    # check if player connect or disconnect
    if number_player_online != len(after_game_rule)-1:
        online_player = OnlinePlayer(number_player_online)
        after_game_rule = game_rule

    # fill game rule for all online player
    for i in game_rule:
        if i != game.player.avatar['id']:
            game_rule_online[i] = game_rule[i]

    # update avatar for each player
    if name_player_online != 0:
        id_player_online = [x for x in game_rule_online]
        name_player_online = [game_rule_online[x]['name'] for x in game_rule_online]
        online_player = OnlinePlayer(number_player_online)

        for i in range(number_player_online):
            online_player.players[f'player{i}'].avatar['id'] = id_player_online[i]
            online_player.players[f'player{i}'].avatar['name'] = name_player_online[i]


# update meteorite and check the death player
def updateMeteorite():
    game.meteorite.rect.x = commitPosition[0]
    game.meteorite.rect.y = commitPosition[1]
    game.meteorite.animation()

    if game.meteorite.deathPlayer():
        game.screenRun = False


# execute event if btn on pressed
def keyboardEvent():
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

    for Btn in game.player.btnPressed:
        if game.player.btnPressed.get(Btn) and Btn in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            eventKeysPressed.get(Btn)()
            game.CallEvent(game.allEvent[1], game.player.avatar)
            break


def displayElement():
    if number_player_online != 0:
        for i, id_ in enumerate(game_rule_online):
            online_player.players[f'player{i}'].UserNameImg = pygame.font.SysFont('font/Prompt-Bold.ttf', 20).render(online_player.players[f'player{i}'].avatar['name'], True, (255, 255, 255))
            online_player.players[f'player{i}'].rect.x = game_rule_online[id_]['position'][0]
            online_player.players[f'player{i}'].rect.y = game_rule_online[id_]['position'][1]
            screen.blit(online_player.players[f'player{i}'].image, online_player.players[f'player{i}'].rect)
            screen.blit(online_player.players[f'player{i}'].UserNameImg, (online_player.players[f'player{i}'].rect.x, online_player.players[f'player{i}'].rect.y-15))

    screen.blit(game.meteorite.image, game.meteorite.rect)
    screen.blit(game.player.image, game.player.rect)
    screen.blit(game.player.TitleUsername, (20, 20))
    screen.blit(game.player.UserNameImg, (game.player.rect.x+10, game.player.rect.y-15))
    pygame.display.update()


# close all and call server for disconnect
def quitGame():
    pygame.quit()
    game.CallEvent(game.allEvent[2], game.player.avatar)


if __name__ == '__main__':
    while game.screenRun:
        game_rule = json.loads(game.CallEvent(game.allEvent[3]))
        number_player_online = len(game_rule) - 1
        game_rule_online = {}
        commitPosition = tuple(map(int, game.CallEvent(game.allEvent[4]).split('.')))

        onlinePlayer()
        coloringScreen()
        updateMeteorite()
        keyboardEvent()
        displayElement()

    quitGame()