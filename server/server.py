import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

clients = {}
lock = threading.Lock()


def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")


def broadcast(message, exclude=None):
    with lock:
        for client in clients:
            if client != exclude:
                try:
                    client.send(message.encode())
                except:
                    pass


def handle_client(client_socket, addr):

    username = None

    try:
        while True:

            data = client_socket.recv(1024).decode()

            if not data:
                break

            parts = data.split(" ", 1)
            command = parts[0]

            if command == "JOIN":

                username = parts[1].strip()

                with lock:
                    clients[client_socket] = username

                msg = f"[{get_timestamp()}] [SERVER] {username} joined the chat"
                print(msg)

                broadcast(msg, client_socket)

            elif command == "MSG":

                message = parts[1].strip()

                formatted = f"[{get_timestamp()}] {username}: {message}"

                print(formatted)

                broadcast(formatted, client_socket)

            elif command == "USERS":

                with lock:
                    user_list = ", ".join(clients.values())

                response = f"[SERVER] Connected users: {user_list}"

                client_socket.send(response.encode())

            elif command == "QUIT":
                break

    except:
        pass

    finally:

        with lock:
            if client_socket in clients:

                name = clients[client_socket]
                del clients[client_socket]

                msg = f"[{get_timestamp()}] [SERVER] {name} left the chat"

                print(msg)

                broadcast(msg)

        client_socket.close()


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen(10)

    print(f"Chat server running on port {PORT}")

    while True:

        client_socket, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr)
        )

        thread.start()


if __name__ == "__main__":
    start_server()