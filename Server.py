from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


#Accept incoming connections
def accept_incoming_connections():
    while True:
        client, client_address = server_socket.accept()
        print(f"{client_address} has connected.")
        clients[client] = client_address
        Thread(target=handle_client, args=(client,client_address)).start()


# Function to handle a single client connection
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    # Receive the user's name from the client
    name = client_socket.recv(1024).decode("utf8")
    benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % name
    client_socket.send(bytes(benvenuto, "utf8"))
    msg = "%s si è unito all chat!" % name

    #Send the message to all connected clients
    for socket in clients:
        socket.send(bytes(msg, "utf8"))
    

    while True:

        # Receive the message from the client
        msg = client_socket.recv(1024)
        # Print the received message along with the client name for debugging
        print(f"Received message from {name}: {msg.decode('utf8')}")

        # If the message is {quit} then close the connection
        if msg == bytes("{quit}", "utf8"):
            client_socket.send(bytes("{quit}", "utf8"))
            client_socket.close()
            del clients[client_socket]
            msg = f"{name} has left the chat!"
            for client_socket in clients:
                client_socket.send(msg)

            print(f"{name} has left the chat")
            break
        else:
            # Send the message to all connected clients
            
            for client_socket in clients:
                client_socket.send(msg)

    #Remove client from dictionary and close the connection
    print(f"Connection with {name} ({address}) closed")





# Server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

# Create a TCP/IP socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Dictionary to store client sockets and their names
clients = {}

if __name__ == "__main__":
    server_socket.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server_socket.close()


