import socket
from _thread import *
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10_000
#all_players = {"G37js-Opkw92-Hidn02-kq2sduhd": {'position': [10, 56]}}
all_players = {}

try:
    s.bind((host, port))
except socket.error as e:
    print('Error [line 11]', str(e))
s.listen(5)


def threaded_client(connection):
    while True:
        data = connection.recv(1024)
        if not data: break

        profile = json.loads(data.decode())

        if profile['Event']:
            print(all_players)
            # modify 'all player' game
            if profile['Event'] == 'players:death':
                all_players.pop(profile['id'])
                connection.sendall(b'200')
            elif profile['Event'] == 'players:new':
                all_players[profile['id']] = {'position': profile['position']}
                connection.sendall(str.encode(json.dumps(all_players)))
            elif profile['Event'] == 'players:move':
                all_players[profile['id']]['position'] = profile['position']
                connection.sendall(b'200')
            elif profile['Event'] == 'get:rule':
                connection.sendall(str.encode(json.dumps(all_players)))

while True:
    Client, address = s.accept()
    start_new_thread(threaded_client, (Client,))
