import Pyro4
import re

@Pyro4.expose
class InsultFilter:
    def __init__(self):
        self.petitions = []
        self.resolutions = []
        daemon = Pyro4.Daemon(host='localhost')
        ns = Pyro4.locateNS(host='localhost', port=9090)
        self.insult_server = ns.lookup('insult.service')
    
    def add_petition(self, message):
        self.petitions.append(message)
        print(f"Adding new message {message}")
        return f"Adding new message {message}"
    
    def get_petitions(self):
        print("Returing to the client the petitions that are currently on the db")
        return self.petitions

    def resolve_petition(self):
        if len(self.petitions) > 0:
            message = self.petitions.pop(0)
            for insult in self.get_insult_list():
                if insult in message:
                    message = message.replace(insult, "CENSORED")
            self.resolutions.append(message)
            print(f"Resolution done: {message}")
            return f"Resolution done: {message}"
        else:
            print("No job to be done")
            return "No job to be done"

    def get_insult_list(self):
        server = Pyro4.Proxy(self.insult_server)
        insult_list = server.get_insults()
        return insult_list
    
    def get_resolutions(self):
        print("Returning to client the resolutions")
        return self.resolutions
    
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('insult.service')
filter = daemon.register(InsultFilter())
ns.register('insult.filter', filter)
print(f"Server uri {uri}")
print(f"Filter uri {filter}")
daemon.requestLoop()