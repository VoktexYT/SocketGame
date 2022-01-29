import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10_000

while True:
    try:
        s = socket.socket()
        host = socket.gethostname()
        port = 10_000
        s.connect((host, port))
        message = s.recv(1024).decode()
        print(message)

        s.close()
    except:
        pass