from IPython.parallel import Client

def fct(x):
    time.sleep(1)
    return x*x

def paraFct():
    client = Client()
    with client[:].sync_imports():import time
    return client[:].map_sync(fct, range(8))
