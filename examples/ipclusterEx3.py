from IPython.parallel import Client
client = Client()
with client[:].sync_imports():import socket, time
%px print(socket.gethostname())

def fct(x):
    time.sleep(1)
    return x*x

client[:].map_sync(fct, range(8))
