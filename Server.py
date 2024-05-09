# importing required libraries.
import socket
from threading import Thread

# define IP and port for server.
host = "localhost"
port = 8080

clients = {}  # clients dict to store information about clients connection.

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set configuration so that many clients can request on one single port.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the IP and port to the socket object.
sock.bind((host, port))


def handle_clients(conn):
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
            conn.send(bytes("/quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(f"{name} has left the chat room", "utf8"))
            break



# send the message to the all connected clients.
def broadcast(msg, prefix=""):
    for client in clients:  # clients is dict that save client's connection info
        client.send(bytes(prefix, "utf8") + msg)


def accept_client_connection():
    while True:  # accept client's request
        client_conn, client_address = sock.accept()  # accept client request
        print(client_address, " has Connected")

        # send a welcome message to the client and ask for name from it.
        client_conn.send(bytes("Welcome to the chat room, Please type your name to continue", "utf8"))
        clients[client_conn] = client_address
        # start the handle clients function in a thread.
        Thread(target=handle_clients, args=(client_conn,)).start()


if __name__ == "__main__":
    # server is listening........
    sock.listen(5)  # here we are accepting max of three clients at once.
    print("listening on port : ", port, "......")

    # start the accept function into thread for handle multiple request at once.
    t = Thread(target=accept_client_connection)

    t.start()  # start thread
    t.join()  # thread wait for main thread to exit.
    sock.close()  # close the socket connection.