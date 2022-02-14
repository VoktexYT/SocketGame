import socket
from _thread import *
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10_000
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
            # modify 'all player' game
            if profile['Event'] == 'players:death':
                all_players.pop(profile['id'])
                connection.sendall(b'200')
            elif profile['Event'] == 'players:new':
                all_players[profile['id']] = {}
                connection.sendall(b'200')
            elif profile['Event'] == 'players:move':
                all_players[profile['id']]['position'] = profile['position']
                connection.sendall(b'200')

            # return value to the client
            elif profile['Event'] == 'get:players':
                connection.sendall(str.encode(json.dumps(all_players)))
            elif profile['Event'] == 'get:players:id':
                allId = ''
                for playerId in all_players:
                    allId += playerId+':'
                allId = allId[:-1]
                connection.sendall(str.encode(allId))
            elif profile['Event'] == 'get:players:position':
                pass
        else:
            print('error, he not event in "Event" key')

        print(all_players)
while True:
    Client, address = s.accept()
    start_new_thread(threaded_client, (Client,))
