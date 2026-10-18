
import socket
import threading

PORT = 65431
SERVER = "172.30.12.162"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def receive(client):
    while True:
        msg = client.recv(2048)

        if not msg:
            break

        print("\n" + msg.decode(FORMAT))


def send(client, msg):
    client.sendall(msg.encode(FORMAT))


def start():
    answer = input("Would you like to connect (yes/no)? ")

    if answer.lower() != "yes":
        return

    connection = connect()

    receive_thread = threading.Thread(
        target=receive,
        args=(connection,),
        daemon=True
    )
    receive_thread.start()

    while True:
        msg = input("Message (q for quit): ")

        if msg.lower() == "q":
            break

        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    connection.close()
    print("Disconnected")


start()
