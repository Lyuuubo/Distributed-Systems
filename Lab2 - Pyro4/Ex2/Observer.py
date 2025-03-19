import Pyro4

@Pyro4.expose
class Observer:
    def notify(self, mss):
        print(f"Message: {mss}")

if __name__ == '__main__':
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS(host='localhost', port=9090)
    uri = ns.lookup('example.observable')
    obj = Pyro4.Proxy(uri)
    obs = daemon.register(Observer)
    print(obj.addObserver(obs))
    #obj.notifyObservers("Perro")
    daemon.requestLoop()