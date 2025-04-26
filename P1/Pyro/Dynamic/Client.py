import Pyro4

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('master.service')
server = Pyro4.Proxy(uri)
number = server.get_resolver_slave()
pyroname = "insult" + str(number) + ".service"
uri = ns.lookup(pyroname)
slave = Pyro4.Proxy(uri)
slave.clean_insults()
slave.add_insult("Fiumba")
print(slave.get_insults())