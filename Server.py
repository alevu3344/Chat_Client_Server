import socket
import threading

# Function to handle a single client connection
def handle_client(client_socket, address):
    print(f"New connection from {address}")

    # Ask for the user's name
    while True:
        client_socket.send("Enter your name: ".encode())
        name = client_socket.recv(1024).decode()

        # Check if the name is already in use
        if name in clients.values():
            client_socket.send("Name already in use. Please enter a different name.".encode())
        else:
            break

    # Add client name and socket to the dictionary
    clients[client_socket] = name

    while True:
        try:
            # Receive message from the client
            data = client_socket.recv(1024)
            
            if not data:
                break

            # Print the received message along with the client name for debugging
            print(f"{name} sent: {data.decode()}")

            # Send the message to all connected clients except the sender
            for socket, client_name in list(clients.items()):  # Iterate over a copy of the dictionary
                if socket != client_socket:  # Exclude the sender
                    try:
                        socket.send((name + ": " + data.decode()).encode())  # Encode string to bytes before sending
                    except:
                        del clients[socket]

        except Exception as e:
            print(f"Error while handling client {address}: {e}")
            break

    # Remove client from dictionary and close the connection
    del clients[client_socket]
    client_socket.close()
    print(f"Connection with {name} ({address}) closed")

# Server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

# Dictionary to store client sockets and their names
clients = {}

while True:
    # Accept a new connection
    client_socket, address = server_socket.accept()

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
