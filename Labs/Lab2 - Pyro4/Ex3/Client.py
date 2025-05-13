import Pyro4

if __name__ == '__main__':
    ns = Pyro4.locateNS(host='localhost', port=9090)
    uri = ns.lookup('example.remote.object')
    obj = Pyro4.Proxy(uri)
    print(obj.greet())
    print(obj.add())
    print(f"Object methods: {obj._pyroMethods}")
