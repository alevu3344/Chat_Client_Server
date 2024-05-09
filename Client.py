import socket
from threading import Thread
import tkinter as tk

def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:
            break

def connect_to_server():
    global s
    host = host_entry.get()
    port = int(port_entry.get())
    name = name_entry.get()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(bytes(name, "utf8"))
        connect_button.config(state=tk.DISABLED)
        host_entry.config(state=tk.DISABLED)
        port_entry.config(state=tk.DISABLED)
        name_entry.config(state=tk.DISABLED)
        receive_thread = Thread(target=receive)
        receive_thread.start()
    except Exception as e:
        msg_list.insert(tk.END, f"Failed to connect: {e}")

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))
    if msg.lower() == '/quit':
        s.close()
        window.quit()

def on_closing(event=None):
    my_msg.set("/quit")
    send()

window = tk.Tk()
window.title("Chat Application")
window.configure(bg="#f0f0f0")

message_frame = tk.Frame(window, height=400, width=600, bg='#ffffff')
message_frame.pack(pady=10)

my_msg = tk.StringVar()
my_msg.set("")

scroll_bar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, height=15, width=70, bg="#ffffff", yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()

entry_frame = tk.Frame(window, bg="#f0f0f0")
entry_frame.pack(pady=5)

host_label = tk.Label(entry_frame, text="Host:", bg="#f0f0f0")
host_label.grid(row=0, column=0, padx=5)

host_entry = tk.Entry(entry_frame)
host_entry.grid(row=0, column=1, padx=5)

port_label = tk.Label(entry_frame, text="Port:", bg="#f0f0f0")
port_label.grid(row=0, column=2, padx=5)

port_entry = tk.Entry(entry_frame)
port_entry.grid(row=0, column=3, padx=5)

name_label = tk.Label(entry_frame, text="Name:", bg="#f0f0f0")
name_label.grid(row=0, column=4, padx=5)

name_entry = tk.Entry(entry_frame)
name_entry.grid(row=0, column=5, padx=5)

connect_button = tk.Button(entry_frame, text="Connect", font=("Arial", 12), fg="white", bg="#007bff", command=connect_to_server)
connect_button.grid(row=0, column=6, padx=5)

entry_field = tk.Entry(window, textvariable=my_msg, fg="black", width=50)
entry_field.pack(pady=5)
entry_field.bind("<Return>", send)

send_button = tk.Button(window, text="Send", font=("Arial", 12), fg="white", bg="#007bff", command=send)
send_button.pack(pady=5)

tk.mainloop()
