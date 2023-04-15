import socket
import threading


HEADER = 64
PORT = 4444
host = socket.gethostbyname(socket.gethostname())
ADDR = (host,PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(ADDR)

server.listen() 

clients= []
nicknames = []
print(f"{host} Server stated!!!")
# broadcasting
def broadcast(message):
    for client in clients:
        client.send(message)

# handle client connection  
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client,address = server.accept()
        print(f"connected with {str(address)}")
        
        client.send('nickname'.encode('ascii'))
        nickname  =client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"Nickname of the client is {nickname} ")
        broadcast(f"{nickname} joined the chat !".encode('ascii'))
        client.send("Connected to server!!".encode('ascii'))
        
        # same time client send something so process that use threading
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
        
    
receive()
            
