import Pyro4
import time
import json
from multiprocessing import Process
from InsultFilter import InsultFilter
from InsultSlave import InsultSlave

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultSlaveFilter(InsultSlave, InsultFilter):

    def __init__(self):
        super().__init__()

slave = InsultSlaveFilter()

# We register the slave for the client to connect to it
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(slave)
print(slave.id)
ns.register("insult" + str(slave.id) + ".service", uri)
print(f"Server uri: {uri}")

# We initialize the heartbeat
p = Process(target=slave.send_info)
p.start()

daemon.requestLoop()