import socket
from threading import Thread
import threading
import tkinter as tk
import sys

connected = False
receive_thread = None  # Initialize receive_thread globally

def receive():
    global receive_thread  # Declare receive_thread as global to modify it inside the function
    while True:
        try:
            msg = s.recv(1024).decode("utf8")
            if not msg:  # Check if msg is empty, indicating the socket is closed
                break
            msg_list.insert(tk.END, msg)
        except OSError:
            break




def connect_to_server():
    global s, connected, receive_thread
    host = host_entry.get()
    port = port_entry.get()
    name = name_entry.get()
    
    # Check if any of the fields are empty
    if not all([host, port, name]):
        msg_list.insert(tk.END, "Please fill in all fields.")
        return
    
    try:
        port = int(port)  # Convert port to int
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(bytes(name, "utf8"))
        connect_button.config(state=tk.DISABLED)
        host_entry.config(state=tk.DISABLED)
        port_entry.config(state=tk.DISABLED)
        name_entry.config(state=tk.DISABLED)
        
        # Create a new receive_thread each time the client connects
        receive_thread = Thread(target=receive)
        receive_thread.start()
        connected = True

    except Exception as e:
        msg_list.insert(tk.END, f"Failed to connect: {e}")


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))
    if msg.lower() == '/quit':
        s.close()
        host_entry.config(state=tk.NORMAL)
        port_entry.config(state=tk.NORMAL)
        name_entry.config(state=tk.NORMAL)
        connect_button.config(state=tk.NORMAL)

def quit_chat():
    global connected
    connected = False
    my_msg.set("/quit")
    send()

def on_closing(event=None):
    global connected, receive_thread
    if connected:
        quit_chat()
    window.destroy()
    # Stop the receive thread if it's running
    if receive_thread.is_alive():
        receive_thread.join(timeout=1)  # Wait for the thread to finish with a timeout
    sys.exit()  # Exit the Python process


window = tk.Tk()
window.title("Chat Application")
window.configure(bg="#f0f0f0")

message_frame = tk.Frame(window, height=500, width=800, bg='#ffffff')
message_frame.pack(pady=20)

my_msg = tk.StringVar()
my_msg.set("")

scroll_bar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, height=20, width=90, bg="#ffffff", yscrollcommand=scroll_bar.set, font=("Helvetica", 12))
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
scroll_bar.config(command=msg_list.yview)

entry_frame = tk.Frame(window, bg="#f0f0f0")
entry_frame.pack(pady=10)

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

connect_button = tk.Button(entry_frame, text="Connect", font=("Helvetica", 12), fg="white", bg="#007bff", command=connect_to_server)
connect_button.grid(row=0, column=6, padx=10)

entry_field = tk.Entry(window, textvariable=my_msg, fg="black", width=80, font=("Helvetica", 12))
entry_field.pack(pady=10)
entry_field.bind("<Return>", send)

send_button = tk.Button(window, text="Send", font=("Helvetica", 12), fg="white", bg="#007bff", command=send)
send_button.pack(pady=5)

quit_button = tk.Button(window, text="Quit", font=("Helvetica", 12), fg="white", bg="#ff0000", command=quit_chat)
quit_button.pack(pady=5)

window.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()
