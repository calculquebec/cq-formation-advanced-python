from IPython.parallel import Client

client = Client()
client.ids

def fct():
    return 'hello'

client[:].apply_sync(fct)

quit()
