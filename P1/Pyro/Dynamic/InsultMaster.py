import Pyro4
import json
import time
from multiprocessing import Manager, Process

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultMaster:

    def __init__(self, shared_slave_list):
        self.slave_list = shared_slave_list
        self.next_id = 0

    def get_resolver_slave(self):

        # We return the id of the oldest pulse of the slave actived that we recieved 
        sorted_by_time = dict(sorted(self.slave_list.items(), key=lambda item: item[1]["last_seen"]))
        filtered_by_time = {k: v for k, v in sorted_by_time.items() if v["active"] is True}
        slave_keys = list(filtered_by_time.keys())
        return (slave_keys[0])

    def heartbeat_slave(self, raw_slave_data):

        # We recieve the heartbeat of each insult slave server
        slave_data = json.loads(raw_slave_data)
        slave_id = int(slave_data["id"])
        slave_pulse = int(slave_data["pulse"])

        # We register that the slave is still active
        self.slave_list[slave_id] = {
            "active" : True,
            "last_seen" : slave_pulse
        }

    def check_slave(self, timeout=10):
        while True:
            time.sleep(1)
            now = time.time()

            # For each slave registered
            for slave in list(self.slave_list.keys()): 
                # Check if the last pulse was 10 seconds ago
                if now - self.slave_list[slave]["last_seen"] > timeout:
                    self.slave_list.pop(slave)
                    

    def next_identifier(self):
        if len(self.slave_list) < 3:
            self.next_id = self.next_id + 1
            return self.next_id
        else:
            return None
        

# We share the dictionary for the slave process
manager = Manager()
shared_slave_list = manager.dict()

# We register the master for the client to connect it
master = InsultMaster(shared_slave_list)
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(master)
ns.register('master.service', uri)
print(f"Server uri: {uri}")

# We create the process of check_slave to verify if the slaves are still alive
p = Process(target=master.check_slave)
p.start()

daemon.requestLoop()