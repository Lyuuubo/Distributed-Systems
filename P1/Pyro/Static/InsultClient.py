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
client = daemon.register(InsultClient)
print(server.add_subscriber(client))
server.add_insults("idiota")
server.add_insults("inútil")
server.add_insults("tonto")
server.add_insults("imbécil")
server.add_insults("patán")
server.add_insults("pesado")
server.add_insults("torpe")
server.add_insults("payaso")
server.add_insults("estúpido")
server.add_insults("malcriado")
print(server.get_insults())
daemon.requestLoop()