# Import
import socket
from _thread import start_new_thread
import json

# default value
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10_000
all_players = {}

# try connection
try:
    s.bind((host, port))
except socket.error as e:
    print('Error [line 11]', str(e))
s.listen(5)


# function called for each player
def threaded_client(connection):
    while True:

        # get information port: 10_000
        data = connection.recv(1024)
        if not data:
            break
        profile = json.loads(data.decode())

        # modify 'all player' game if event is not empty
        if profile['Event']:
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


def Server():
    Client, address = s.accept()
    start_new_thread(threaded_client, (Client,))


if __name__ == '__main__':
    while True:
        Server()
