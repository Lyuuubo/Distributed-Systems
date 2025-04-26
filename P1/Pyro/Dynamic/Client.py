import Pyro4

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('master.service')
print(uri)
server = Pyro4.Proxy(uri)
print(server.get_resolver_slave())