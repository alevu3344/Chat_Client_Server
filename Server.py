import socket
from threading import Thread
import threading
import argparse  # Importing argparse module for parsing command-line arguments

def handle_client(conn, addr):
    try:
        name = conn.recv(1024).decode("utf8")
        welcome = f"Welcome {name}. Good to see you :)"
        conn.send(bytes(welcome, "utf8"))
        msg = name + " has recently joined us"
        broadcast(bytes(msg, "utf8"))

        clients[conn] = name

        while True:
            msg = conn.recv(1024)
            if msg != bytes("/quit", "utf8"):
                broadcast(msg, name + ": ")
            else:
                raise ConnectionError()
    except ConnectionError:
        conn.close()
        del clients[conn]
        broadcast(bytes(f"{name} has left the chat room", "utf8"))
        print(f"{name} has left the chat room")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        # Terminate the receive thread associated with this client
        for client_conn, client_name in list(clients.items()):
            if client_name == name:
                del clients[client_conn]
                break
        # Terminate the receive thread associated with this client
        for thread in threading.enumerate():
            if thread.name == f"Thread-{addr}":
                thread.join()
                break

def broadcast(msg, prefix=""):
    for client in clients:
        try:
            client.send(bytes(prefix, "utf8") + msg)
        except Exception as e:
            print(f"Error broadcasting message to a client: {e}")

def accept_client_connections():
    while True:
        try:
            client_conn, client_addr = sock.accept()
            print(client_addr, " has Connected")
            clients[client_conn] = client_addr
            Thread(target=handle_client, args=(client_conn, client_addr)).start()
        except Exception as e:
            print(f"Error accepting client connection: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument("--host", type=str, default="localhost", help="Host address")
    parser.add_argument("--port", type=int, default=8080, help="Port number")
    args = parser.parse_args()

    host = args.host
    port = args.port

    clients = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    try:
        sock.listen(5)
        print(f"Listening on {host}:{port}")
        accept_thread = Thread(target=accept_client_connections)
        accept_thread.start()
        accept_thread.join()
    except KeyboardInterrupt:
        print("Server shutting down...")
        for client_conn in clients:
            client_conn.close()
        sock.close()
