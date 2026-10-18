import threading
import socket
from collections import defaultdict
import random
import time

# Get all the usernmaes from the username.txt file
all_username = []

with open("usernames.txt","r") as file:
    for line in file:
        if line.strip():
            all_username.append(line.strip())


PORT = 65431
SERVER = "172.30.12.162"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(ADDR)

clients = defaultdict(tuple)
clients_lock = threading.Lock()


def handle_client(username):
    print(f"-----------------------------{username} Connected---------------------------")
    conn = clients[username][0]
    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            
            if msg == DISCONNECT_MESSAGE:
                connected = False
                msg = f"-----------------------------{username} Disconnected---------------------------"
            else:
                msg = f"[{username} | {time.ctime()}] {msg}"
            
            print(msg)
            with clients_lock:
                for client_username, client_info in clients.items():
                    c = client_info[0]
                    c.sendall(msg.encode(FORMAT))

    finally:
        with clients_lock:
            del clients[username]

        conn.close()
    


def start():
    print('[SSERVER] Starting ........')
    server.listen()
    username_no = 0
    while True:
        conn, addr = server.accept()
        client_username = all_username[username_no]
        username_no += 1
        with clients_lock:
            clients[client_username] = (conn,addr)
        thread = threading.Thread(target=handle_client, args=(client_username,))
        thread.start()


start()