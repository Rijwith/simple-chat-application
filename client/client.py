import socket
import threading
import sys

SERVER_IP = input("Enter server IP: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

username = input("Enter username: ")

client.send(f"JOIN {username}".encode())


def receive_messages():

    while True:

        try:

            message = client.recv(1024).decode()

            if not message:
                break

            print(message)

        except:
            print("Disconnected from server")
            client.close()
            break


def send_messages():

    while True:

        msg = input()

        if msg == "/quit":

            client.send("QUIT".encode())
            client.close()
            sys.exit()

        elif msg == "/users":

            client.send("USERS".encode())

        else:

            client.send(f"MSG {msg}".encode())


thread = threading.Thread(target=receive_messages)

thread.start()

send_messages()