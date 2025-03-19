import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

# Print list of available methods
print(s.system.listMethods())
print(s.add_observer('http://localhost:8001'))
print(s.add_insults("negro"))
print(s.add_observer('http://localhost:8002'))
print(s.add_insults("perro"))
print(s.add_observer('http://localhost:8003'))
print(s.add_insults("kevin"))
print(s.add_insults("lyubo"))