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
        dead_clients = []

        for client in list(clients):
            if client != exclude:
                try:
                    client.send(message.encode())
                except:
                    dead_clients.append(client)

        for dc in dead_clients:
            if dc in clients:
                del clients[dc]
                try:
                    dc.close()
                except:
                    pass


def handle_client(client_socket, addr):

    username = None
    has_left = False

    try:
        while True:

            data = client_socket.recv(1024).decode()

            if not data:
                break

            parts = data.split(" ", 1)
            command = parts[0].upper().lstrip("/")
            argument = parts[1].strip() if len(parts) > 1 else ""

            if command == "JOIN":

                username = argument

                with lock:
                    clients[client_socket] = username

                msg = f"[{get_timestamp()}] [SERVER] {username} joined the chat"
                print(msg)

                broadcast(msg, client_socket)

            elif command == "MSG":

                if username:
                    formatted = f"[{get_timestamp()}] {username}: {argument}"
                    print(formatted)

                    broadcast(formatted, client_socket)

            elif command == "QUIT":

                if username:
                    msg = f"[{get_timestamp()}] [SERVER] {username} left the chat"
                    print(msg)

                    broadcast(msg, client_socket)

                has_left = True
                break

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:

        with lock:
            if client_socket in clients:
                name = clients[client_socket]
                del clients[client_socket]

                if not has_left:
                    msg = f"[{get_timestamp()}] [SERVER] {name} left the chat"
                    print(msg)

                    broadcast(msg, client_socket)

        try:
            client_socket.close()
        except:
            pass


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(10)

    print(f"Chat server running on port {PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr)
        )
        thread.start()


if __name__ == "__main__":
    start_server()
