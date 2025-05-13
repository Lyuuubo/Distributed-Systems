import Pyro4

if __name__ == '__main__':
    ns = Pyro4.locateNS(host='localhost',port=9090) # Llarga
    uri = ns.lookup('echo.server')                  # Llarga
    obj = Pyro4.Proxy(uri)        # amb uri
    print(obj.echo("Hola"))
