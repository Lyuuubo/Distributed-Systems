import Pyro4
import time

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

time.sleep(10)
print(slave.kill_broadcast())
print(slave.kill_broadcast())
print(slave.get_insults())