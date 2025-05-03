import Pyro4
import time
import json
from InsultFather import InsultFather

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultSlave(InsultFather):

    def __init__(self):
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('insult.service')
        server = Pyro4.Proxy(uri)
        self.id = server.next_identifier()
        super().__init__()

    def send_info(self):

        # We establish the connection with the master server
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('insult.service')
        server = Pyro4.Proxy(uri)

        print("Sending information to master...")
        # We proceed to do the hearbeat, to notify to the master server that the slave is still connected
        while True:
            raw_slave_data = {
                "id" : self.id,
                "pulse" : time.time(),
                "is_filter" : self.is_filter
            }
            server.heartbeat_slave(json.dumps(raw_slave_data))
            time.sleep(3)

