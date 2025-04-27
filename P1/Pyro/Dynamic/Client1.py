import Pyro4

@Pyro4.expose
class InsultClient:

    def notify_sub(self, message):
        print(f"Message recieved: {message}")

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('master.service')
server = Pyro4.Proxy(uri)
uri = ns.lookup("insult" + str(server.get_resolver_slave()) + ".service")
slave = Pyro4.Proxy(uri)

slave.clean_subscribers()
client = daemon.register(InsultClient)
print(slave.add_subscriber(client))

slave.clean_insults()
slave.add_insult("Fiumba")
print(slave.get_insults())
print(slave.start_broadcast())

daemon.requestLoop()

