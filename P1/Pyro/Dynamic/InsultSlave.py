import Pyro4
import time
import json
import threading
from InsultService import InsultService

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultSlave(InsultService):

    def __init__(self, id):
        self.petitions_queue = []
        self.id = id
        super().__init__()

    def send_info(self):

        # We establish the connection with the master server
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('master.service')
        server = Pyro4.Proxy(uri)

        print("Sending information to master...")
        # We proceed to do the hearbeat 
        while True:
            raw_slave_data = {
                "id" : self.id,
                "data" : len(self.petitions_queue)
            }
            server.heartbeat_slave(json.dumps(raw_slave_data))
            time.sleep(5)

# We initialize the heartbeat
slave = InsultSlave(id=1)
thread = threading.Thread(target=slave.send_info, daemon=True)
thread.start()

# We register the slave for the client to connect to it
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(InsultSlave)
ns.register('insult.service', uri)
print(f"Server uri: {uri}")

daemon.requestLoop()