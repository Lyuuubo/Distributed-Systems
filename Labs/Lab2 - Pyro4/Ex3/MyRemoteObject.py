import Pyro4

@Pyro4.expose
class MyRemoteObject:
    def greet(self):
        print("greet")
        return 'Method greet'

    def add(self):
        print("add")
        return 'Method add'

if __name__ == '__main__':
    daemon = Pyro4.Daemon(host='localhost')
    ns = Pyro4.locateNS(host='localhost', port=9090)
    uri = daemon.register(MyRemoteObject)
    ns.register('example.remote.object', uri)
    print(f'URI: {uri}')
    daemon.requestLoop() 
