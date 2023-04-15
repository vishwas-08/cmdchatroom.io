import socket
import threading

HEADER = 64
PORT = 4444
host = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
ADDR = (host,PORT)
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# connect to server
client.connect(ADDR)

nickname = input("Choose a nickname")


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'nickname':
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except:
            print('503 Service Unavailable')
            client.close()
            break
        
def write():
    while True:
        message = f'{nickname}:{input("")}'
        client.send(message.encode('ascii'))
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread =  threading.Thread(target=write)
write_thread.start()
