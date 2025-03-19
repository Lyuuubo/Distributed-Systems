import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

# Print list of available methods
print(s.system.listMethods())
print(s.add_insults("cap d'espinaca"))
print(s.add_insults("tonto"))
print(s.add_insults("moolt tonto"))
print(s.add_insults("perro"))
print(s.get_insults())
print(s.insult_me())