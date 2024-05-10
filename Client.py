import socket
from threading import Thread
import tkinter as tk
import sys

# Global variables to track connection status and receive thread
connected = False
receive_thread = None

# Function to receive messages from the server
def receive():
    global receive_thread
    while True:
        try:
            msg = s.recv(1024).decode("utf8")  # Receive message from server
            if not msg:  # If message is empty, indicating socket is closed
                break
            msg_list.insert(tk.END, msg)  # Insert message into the message listbox
        except OSError:
            break

# Function to connect to the server
def connect_to_server():
    global s, connected, receive_thread
    host = host_entry.get()  # Get host address from entry
    port = port_entry.get()  # Get port number from entry
    name = name_entry.get()  # Get client name from entry
    
    # Check if any of the fields are empty
    if not all([host, port, name]):
        msg_list.insert(tk.END, "Please fill in all fields.")
        return
    
    try:
        port = int(port)  # Convert port to int
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket object
        s.connect((host, port))  # Connect to server
        s.send(bytes(name, "utf8"))  # Send client name to server
        # Disable connect button and entry fields, enable send and quit buttons
        connect_button.config(state=tk.DISABLED)
        host_entry.config(state=tk.DISABLED)
        port_entry.config(state=tk.DISABLED)
        name_entry.config(state=tk.DISABLED)
        send_button.config(state=tk.NORMAL)
        quit_button.config(state=tk.NORMAL)
        # Create a new receive thread each time the client connects
        receive_thread = Thread(target=receive)
        receive_thread.start()
        connected = True  # Set connection status to True

    except Exception as e:
        msg_list.insert(tk.END, f"Failed to connect: {e}")

# Function to send message to the server
def send(event=None):
    msg = my_msg.get()  # Get message from entry field
    my_msg.set("")  # Clear entry field
    s.send(bytes(msg, "utf8"))  # Send message to server
    if msg.lower() == '/quit':
        s.close()  # Close socket connection
        # Enable host, port, and name entry fields, disable send and quit buttons
        host_entry.config(state=tk.NORMAL)
        port_entry.config(state=tk.NORMAL)
        name_entry.config(state=tk.NORMAL)
        connect_button.config(state=tk.NORMAL)

# Function to quit chat session
def quit_chat():
    global connected
    connected = False
    # Disable quit and send buttons
    quit_button.config(state=tk.DISABLED)
    send_button.config(state=tk.DISABLED)
    my_msg.set("/quit")  # Set message to '/quit'
    send()  # Call send function

# Function to handle window closing event
def on_closing(event=None):
    global connected, receive_thread
    if connected:
        quit_chat()  # If connected, call quit_chat function
    window.destroy()  # Destroy tkinter window
    # Stop the receive thread if it's running
    if receive_thread.is_alive():
        receive_thread.join(timeout=1)  # Wait for the thread to finish with a timeout
    sys.exit()  # Exit the Python process

# Create tkinter window
window = tk.Tk()
window.title("Chat Application")
window.configure(bg="#f0f0f0")

# Frame to display chat messages
message_frame = tk.Frame(window, height=500, width=800, bg='#ffffff')
message_frame.pack(pady=20)

# Variable to store user message
my_msg = tk.StringVar()
my_msg.set("")

# Scrollbar for message listbox
scroll_bar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, height=20, width=90, bg="#ffffff", yscrollcommand=scroll_bar.set, font=("Helvetica", 12))
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
scroll_bar.config(command=msg_list.yview)

# Frame for entry fields
entry_frame = tk.Frame(window, bg="#f0f0f0")
entry_frame.pack(pady=10)

# Labels and entry fields for host, port, and name
host_label = tk.Label(entry_frame, text="Host:", bg="#f0f0f0", font=("Helvetica", 12))
host_label.grid(row=0, column=0, padx=5)

host_entry = tk.Entry(entry_frame, font=("Helvetica", 12))
host_entry.grid(row=0, column=1, padx=5)

port_label = tk.Label(entry_frame, text="Port:", bg="#f0f0f0", font=("Helvetica", 12))
port_label.grid(row=0, column=2, padx=5)

port_entry = tk.Entry(entry_frame, font=("Helvetica", 12))
port_entry.grid(row=0, column=3, padx=5)

name_label = tk.Label(entry_frame, text="Name:", bg="#f0f0f0", font=("Helvetica", 12))
name_label.grid(row=0, column=4, padx=5)

name_entry = tk.Entry(entry_frame, font=("Helvetica", 12))
name_entry.grid(row=0, column=5, padx=5)

# Connect button to connect to server
connect_button = tk.Button(entry_frame, text="Connect", font=("Helvetica", 12), fg="white", bg="#007bff", command=connect_to_server)
connect_button.grid(row=0, column=6, padx=10)

# Entry field to input messages
entry_field = tk.Entry(window, textvariable=my_msg, fg="black", width=80, font=("Helvetica", 12))
entry_field.pack(pady=10)
entry_field.bind("<Return>", send)

# Send button to send messages
send_button = tk.Button(window, text="Send", font=("Helvetica", 12), fg="white", bg="#007bff", command=send)
send_button.config(state=tk.DISABLED)  # Disable send button initially
send_button.pack(pady=5)

# Quit button to quit chat session
quit_button = tk.Button(window, text="Quit", font=("Helvetica", 12), fg="white", bg="#ff0000", command=quit_chat)
quit_button.config(state=tk.DISABLED)  # Disable quit button initially
quit_button.pack(pady=5)

# Bind window closing event to on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the tkinter event loop
tk.mainloop()
