import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                break

            # Print the received message
            print(data.decode())
        except Exception as e:
            print(f"Error while receiving messages: {e}")
            break

# Server address and port
SERVER_HOST = 'localhost'
SERVER_PORT = 5555

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to the server")

    # Ask for the user's name
    name = input("Enter your name: ")
    client_socket.send(name.encode())

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Send messages to the server
    while True:
        message = input()
        client_socket.send(message.encode())
except Exception as e:
    print(f"Error while connecting to the server: {e}")
finally:
    # Close the socket
    client_socket.close()
