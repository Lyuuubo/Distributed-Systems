import Pyro4
import time

server = Pyro4.Proxy('PYRONAME:insult.service')
filter = Pyro4.Proxy('PYRONAME:insult.filter')
print(server.random_events())
time.sleep(20)
print(server.kill_random_events())
print(server.kill_random_events())