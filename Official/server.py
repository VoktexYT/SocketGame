import socket
from _thread import *
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10_000
all_players = []

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
                all_players.remove(profile['id'])
            elif profile['Event'] == 'new':
                all_players.append(profile['id'])
            elif profile['Event'] == 'move':
                pass
            print(all_players)
        else:
            print('error, he not event in "Event" key')

        reply = 'Hello'
        connection.sendall(str.encode(reply))

# def again():
#     s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = socket.gethostname()
#     port = 10_001
#     s2.bind((host, port))
#     s2.send(b'coucou')
#     s2.close()

while True:
    #again()
    Client, address = s.accept()
    start_new_thread(threaded_client, (Client,))
