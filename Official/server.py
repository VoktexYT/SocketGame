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
    print(str(e))
s.listen(5)


def threaded_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        profile = json.loads(data.decode())

        if profile['Event']:
            if profile['Event'] == 'death':
                all_players.pop(profile['id'])
            elif profile['Event'] == 'new':
                all_players[profile['id']] = {}
            elif profile['Event'] == 'move':
                all_players[profile['id']]['position'] = profile['position']
            print(all_players)
        else:
            print('error, he not event in "Event" key')
        connection.sendall(str.encode(json.dumps(all_players)))


while True:
    Client, address = s.accept()
    start_new_thread(threaded_client, (Client,))
