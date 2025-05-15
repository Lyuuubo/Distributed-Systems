import Pyro4
import random

@Pyro4.expose
class InsultClient:
    def __init__(self):
        self.insults = []

    def notify(self, insult):
        print(f"Recived insult {insult}")
        return insult

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('insult.service')
server = Pyro4.Proxy(uri)
client = InsultClient()
uri = daemon.register(client)
ns.register("insult.client", uri)
daemon.requestLoop()