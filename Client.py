import tkinter as tkt
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            # Receive msg from the server
            msg = client_socket.recv(1024).decode("utf8")
            if not msg:
                break
            msg_list.insert(tkt.END, msg)
        except Exception as e:
            print(f"Error while receiving messages: {e}")
            break

# Function to send a message to the server
def send_message():
    message = my_msg.get()
    if message:
        try:
            client_socket.send(bytes(message, "utf8"))
            my_msg.set("Type your message here")
        except Exception as e:
            print(f"Error while sending message: {e}")



def connect_to_server():
    host = host_entry.get()
    port = int(port_entry.get())
    global name
    name = name_entry.get()

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print("Connected to the server")

        # Send user name to the server
        client_socket.send(name.encode())

        # Start a thread to receive messages from the server
        receive_thread = Thread(target=receive_messages)
        receive_thread.start()
    except Exception as e:
        print(f"Error while connecting to the server: {e}")
        root.destroy()

def quit_chat(event=None):
    my_msg.set("{quit}")
    send_message()

# Create a TCP/IP socket
client_socket = socket(AF_INET, SOCK_STREAM)

root = tkt.Tk()
root.title("Chat_Laboratorio")
root.geometry("800x800")  # Set window size

# Increase font size for all widgets
FONT_SIZE = 14

# Create the Frame to contain messages
messages_frame = tkt.Frame(root)
messages_frame.pack(pady=10)

my_msg = tkt.StringVar()
my_msg.set("")
scrollbar = tkt.Scrollbar(messages_frame)

msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, font=("Helvetica", FONT_SIZE))
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
scrollbar.config(command=msg_list.yview)

# Label and Entry for Host
host_label = tkt.Label(root, text="Host:", font=("Helvetica", FONT_SIZE))
host_label.pack()
host_entry = tkt.Entry(root, font=("Helvetica", FONT_SIZE))
host_entry.pack()

# Label and Entry for Port
port_label = tkt.Label(root, text="Port:", font=("Helvetica", FONT_SIZE))
port_label.pack()
port_entry = tkt.Entry(root, font=("Helvetica", FONT_SIZE))
port_entry.pack()

# Label and Entry for User Name
name_label = tkt.Label(root, text="User Name:", font=("Helvetica", FONT_SIZE))
name_label.pack()
name_entry = tkt.Entry(root, font=("Helvetica", FONT_SIZE))
name_entry.pack()

# Label and Entry for Message
entry_label = tkt.Label(root, text="Message:", font=("Helvetica", FONT_SIZE))
entry_label.pack()
entry_field = tkt.Entry(root, textvariable=my_msg, font=("Helvetica", FONT_SIZE))
entry_field.bind("<Return>", send_message)
entry_field.pack()

# Buttons for Connect and Quit
button_frame = tkt.Frame(root)
button_frame.pack(pady=10)

connect_button = tkt.Button(button_frame, text="Connect", command=connect_to_server, font=("Helvetica", FONT_SIZE))
connect_button.pack(side=tkt.LEFT, padx=10)

quit_button = tkt.Button(button_frame, text="Quit", command=quit_chat, font=("Helvetica", FONT_SIZE))
quit_button.pack(side=tkt.RIGHT, padx=10)

# Send button
send_button = tkt.Button(button_frame, text="Send", command=send_message, font=("Helvetica", FONT_SIZE))
send_button.pack(side=tkt.RIGHT, padx=10)

root.mainloop()
