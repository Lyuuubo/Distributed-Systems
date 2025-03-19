import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Observable:
    def __init__(self):
        self.observers = []

    def addObserver(self, obs):
        self.observers.append(obs)
        print(f'Observer added')
        return 'Added'

    def removeObserver(self, obs):
        self.observers.remove(obs)
        print(f'Observer removed')
        return 'Removed'

    def notifyObservers(self, mss):
        for obs in self.observers:
            con = Pyro4.Proxy(obs)
            con.notify(mss)
        return 'Received message'

if __name__ == '__main__':
    daemon = Pyro4.Daemon(host='localhost')
    ns = Pyro4.locateNS(host='localhost', port=9090)
    uri = daemon.register(Observable)
    ns.register('example.observable', uri)
    daemon.requestLoop()
