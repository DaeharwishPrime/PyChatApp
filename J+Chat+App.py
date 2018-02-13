
# coding: utf-8

# In[6]:


from socket import AF_INET, socket, SOCK_STREAM


# In[7]:


from threading import Thread


# In[8]:


clients = {}


# In[9]:


addresses = {}


# In[10]:


HOST = ''


# In[11]:


PORT = 33000


# In[12]:


BUFSIZ = 1024


# In[13]:


ADDR = (HOST,PORT)


# In[14]:


SERVER = socket(AF_INET, SOCK_STREAM)


# In[16]:


SERVER.bind(ADDR)


# In[19]:


def accept_incoming_connections():
    """sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the Motherland!"+ "Now type that name of yours and press enter!","utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args = (client,)).start()


# In[20]:


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

