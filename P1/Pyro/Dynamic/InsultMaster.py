import Pyro4
import json
import time
from multiprocessing import Manager, Process

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultMaster:

    def __init__(self, shared_slave_list):
        self.slave_list = shared_slave_list
        self.filter_list = {}
        self.next_id = 0

    def get_resolver_slave(self):

        # We return the id of the oldest pulse of the slave actived that we recieved 
        sorted_by_petitions_time = dict(sorted(self.slave_list.items(), key=lambda item: (item[1]["number_petitions"], item[1]["last_seen"])))
        filtered_by_service = {k: v for k, v in sorted_by_petitions_time.items() if v["is_filter"] is False}
        slave_keys = list(filtered_by_service.keys())
        if slave_keys:

            # Updating the number petitions of the slave 
            tmp = self.slave_list[slave_keys[0]]
            tmp["number_petitions"] = tmp["number_petitions"] + 1
            self.slave_list[slave_keys[0]] = tmp

            # We return the url of the slave service
            return "insult" + str(slave_keys[0]) + ".service"
        else:
            return None
        
    def get_resolver_filter(self):

        # We return the id of the oldest pulse of the slave actived that we recieved 
        sorted_by_petitions_time = dict(sorted(self.slave_list.items(), key=lambda item: (item[1]["number_petitions"], item[1]["last_seen"])))
        filtered_by_service = {k: v for k, v in sorted_by_petitions_time.items() if v["is_filter"] is True}
        slave_keys = list(filtered_by_service.keys())
        if slave_keys:
            
            # Updating the number petitions of the slave 
            tmp = self.slave_list[slave_keys[0]]
            tmp["number_petitions"] = tmp["number_petitions"] + 1
            self.slave_list[slave_keys[0]] = tmp

            # We return the url of the filter service
            return "insult" + str(slave_keys[0]) + ".service"
        else:
            return None

    def heartbeat_slave(self, raw_slave_data):

        # We recieve the heartbeat of each insult slave server
        slave_data = json.loads(raw_slave_data)
        slave_id = int(slave_data["id"])
        slave_pulse = int(slave_data["pulse"])
        is_filter = bool(slave_data["is_filter"])

        # We check if the slave is new, if that's the case we set number_petition variable to zero
        if slave_id not in self.slave_list:
            self.slave_list[slave_id] = {
                "last_seen": slave_pulse,
                "is_filter": is_filter,
                "number_petitions" : 0
            }

        # We only update the last_seen variable if the slave is still active
        else: 
            tmp = self.slave_list[slave_id]
            tmp["last_seen"] = slave_pulse
            self.slave_list[slave_id] = tmp

        # We check if the pulse comes from a filter service
        if is_filter:
            # If that's the case we register it to the filter list
            self.filter_list[slave_id] = self.slave_list[slave_id]

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
        # We update the id counter for the slaves
        self.next_id = self.next_id + 1
        return self.next_id
        

# We share the dictionary for the slave process
manager = Manager()
shared_slave_list = manager.dict()

# We register the master for the client to connect it
master = InsultMaster(shared_slave_list)
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(master)
ns.register('master.service', uri)
print(f"Master uri: {uri}")

# We create the process of check_slave to verify if the slaves are still alive
p = Process(target=master.check_slave)
p.start()

daemon.requestLoop()