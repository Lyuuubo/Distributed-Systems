import Pyro4

if __name__ == '__main__':
    obj = Pyro4.Proxy('PYRONAME:example.observable')
    print(obj.notifyObservers("Hello, Observers!"))