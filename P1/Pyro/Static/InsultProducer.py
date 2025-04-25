import Pyro4
import time

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('insult.filter')
filter = Pyro4.Proxy(uri)

while True:
    print(filter.resolve_petitions())
    time.sleep(5)