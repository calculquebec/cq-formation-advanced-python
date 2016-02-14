from IPython.parallel import Client

client = Client()
client.ids

with client[:].sync_imports(): import socket
%px print(socket.gethostname())

quit
