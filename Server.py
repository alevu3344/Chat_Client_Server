import socket
from threading import Thread
import threading
import argparse 

# Function to handle individual client connections
def handle_client(conn, addr):
    try:
        # Receive the client's name
        name = conn.recv(1024).decode("utf8")
        welcome = f"Welcome {name}. Good to see you :)"
        # Send a welcome message to the client
        conn.send(bytes(welcome, "utf8"))
        msg = name + " has recently joined us"
        # Broadcast the joining message to all clients
        broadcast(bytes(msg, "utf8"))

        # Add the client connection to the dictionary of clients
        clients[conn] = name

        # Continuously receive messages from the client and broadcast them
        while True:
            msg = conn.recv(1024)
            # If the client sends '/quit', break out of the loop to disconnect
            if msg != bytes("/quit", "utf8"):
                broadcast(msg, name + ": ")
            else:
                raise ConnectionError()
    except ConnectionError:
        # Handle disconnection by closing the connection and removing the client from the dictionary
        conn.close()
        del clients[conn]
        # Broadcast the disconnection message to all clients
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

# Function to broadcast a message to all connected clients
def broadcast(msg, prefix=""):
    for client in clients:
        try:
            client.send(bytes(prefix, "utf8") + msg)
        except Exception as e:
            print(f"Error broadcasting message to a client: {e}")

# Function to accept incoming client connections
def accept_client_connections():
    while True:
        try:
            client_conn, client_addr = sock.accept()
            print(client_addr, " has Connected")
            clients[client_conn] = client_addr
            # Spawn a new thread to handle the new client
            Thread(target=handle_client, args=(client_conn, client_addr)).start()
        except Exception as e:
            print(f"Error accepting client connection: {e}")

# Entry point of the script
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument("--host", type=str, default="localhost", help="Host address")
    parser.add_argument("--port", type=int, default=8080, help="Port number")
    args = parser.parse_args()

    host = args.host
    port = args.port

    clients = {}  # Dictionary to store connected clients
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    try:
        sock.listen(5)  # Listen for incoming connections
        print(f"Listening on {host}:{port}")
        # Start a thread to handle incoming client connections
        accept_thread = Thread(target=accept_client_connections)
        accept_thread.start()
        accept_thread.join()  # Wait for the accept thread to finish
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully shut down the server
        print("Server shutting down...")
        for client_conn in clients:
            client_conn.close()
        sock.close()
