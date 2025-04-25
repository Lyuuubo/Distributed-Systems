import Pyro4
import json

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultMaster:

    def __init__(self):
        self.slave_list = {}

    def redirect_petitions(self):
        return self.slave_list.get(0)

    def heartbeat_slave(self, raw_slave_data):
        slave_data = json.loads(raw_slave_data)
        print(f"Slave data recieved: {slave_data}")
        slave_id = int(slave_data["id"])
        slave_petitions = int(slave_data["data"])

        self.slave_list[slave_id] = slave_petitions
        auxiliar_list = sorted(self.slave_list.items(), key=lambda item: item[1], reverse=True)
        self.slave_list = dict(auxiliar_list)


daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(InsultMaster)
ns.register('master.service', uri)
print(f"Server uri: {uri}")
daemon.requestLoop()
