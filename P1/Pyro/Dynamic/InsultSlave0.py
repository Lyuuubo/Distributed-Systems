import Pyro4
import time
import json
from multiprocessing import Process
from InsultService import InsultService

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultSlave(InsultService):

    def __init__(self, id):
        self.id = id
        super().__init__()

    def send_info(self):

        # We establish the connection with the master server
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('master.service')
        server = Pyro4.Proxy(uri)

        print("Sending information to master...")
        # We proceed to do the hearbeat, to notify to the master server that the slave is still connected
        while True:
            raw_slave_data = {
                "id" : self.id,
                "pulse" : time.time()
            }
            server.heartbeat_slave(json.dumps(raw_slave_data))
            time.sleep(5)

# We initialize the heartbeat
slave = InsultSlave(id=0)
p = Process(target=slave.send_info)
p.start()


# We register the slave for the client to connect to it
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(InsultSlave)
ns.register('insult.service', uri)
print(f"Server uri: {uri}")

daemon.requestLoop()