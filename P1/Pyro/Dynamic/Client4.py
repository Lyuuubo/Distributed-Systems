import Pyro4
import time

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('master.service')
server = Pyro4.Proxy(uri)
number = server.get_resolver_filter()
print(number)
uri = ns.lookup("insult" + str(number) + ".service")
slave = Pyro4.Proxy(uri)
print(uri)

slave.clean_resolutions()
