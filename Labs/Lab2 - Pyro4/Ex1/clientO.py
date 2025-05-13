import Pyro4

ns = Pyro4.locateNS(host='192.168.6.111',port=9090) # Llarga
uri = ns.lookup('elnegro')                  # Llarga
obj = Pyro4.Proxy(uri)  #Forma curta
print(obj.echo("Kevin negro"))

