
# coding: utf-8

# ## The Server

# In[ ]:


from socket import AF_INET, socket, SOCK_STREAM


# In[ ]:


from threading import Thread


# In[ ]:


clients = {}


# In[ ]:


addresses = {}


# In[ ]:


HOST = ''


# In[ ]:


PORT = 33000


# In[ ]:


BUFSIZ = 1024


# In[ ]:


ADDR = (HOST,PORT)


# In[ ]:


SERVER = socket(AF_INET, SOCK_STREAM)


# In[ ]:


SERVER.bind(ADDR)


# In[ ]:


def accept_incoming_connections():
    """sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the Motherland!"+ "Now type that name of yours and press enter!","utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args = (client,)).start()


# In[ ]:


def handle_client(client): #Takes Client Socket As Argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client]=name
    while True:
        msg = client.recv(BUFSIZ)
        if msg !=bytes("{quit}","utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


# In[ ]:


def broadcast(msg,prefix=""): #Prefix is for name identification.
    """broadcasts messages to tall clients."""
    for sock in clients:
        sock.send(bytes(prefix,"utf8")+msg)


# In[ ]:


if __name__ == "__main__":
    SERVER.listen(5) #listens for up to 5 connections.
    print("Waiting for connection...")
    ACCEPT_THREAD=Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() #Starts infinite loop.
    break
    ACCEPT_THREAD.join()
    SERVER.close()


# ## The Client

# In[ ]:


#!/usr/bin/env python3
"""Script for Tkinter GUI chat client"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


# In[ ]:


def receive():
    """Handles message receipt."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: #Possible that Client has left chat.
            break


# In[ ]:


def send(event=None): #Event is passed by binders.
    #handles sending messages
    msg=my_msg.get()
    my_msg.set("") #Clears input field
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


# In[1]:


def on_closing(event=None): #Called when window is closed
    my_msg.set("{quit}")
    send()


# In[ ]:


top = tkinter.Tk()
top.title("Chattinest Chat")


# In[ ]:


messages_frame=tkinter.Frame(top)
my_msg = tkinter.StringVar() #For messages to be sent
my_msg.set("Me")
scrollbar=tkinter.Scrollbar(messages_frame) #Provides History


# In[ ]:


msg_list = tkinter.Listbox(messages_frame, height=15, width=50), 
yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter,LEFT, fill.tkinter.BOTH)
msg_list.pack()

messages_frame.pack()


# In[ ]:


entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send) #when you press enter your message will send
entry_field.pack()
send_button=tkinter.Button(top, text="Send", command=send) #also a send button 
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


# In[ ]:


HOST=input('Enter Host: ') 
#apparently additional GUI exists so I can do this more easily
PORT=input('Enter port: ')

if not PORT:
    PORT=33000 #default
else:
    PORT = int(PORT)
    
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket=socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


# In[ ]:


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() #starts GUI execution

