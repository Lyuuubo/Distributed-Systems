import Pyro4
import re

@Pyro4.expose
class InsultFilter:
    def __init__(self, uri):
        self.petitions = []
        self.resolutions = []
        self.insult_list = []
        self.insult_server = uri
    
    def add_petitions(self, message):
        if message not in self.petitions:
            print(f"Adding new message {message}")
            self.petitions.append(message)

    def resolve_petitions(self):
        message = self.petitions.pop()
        self.insult_list = self.get_insult_list(self.insult_server)
        res = ""
        for word in re.split(r'[,.:;!?¡¿\s]+', message):
            if word in self.insult_list:
                aux_word = "CENSORED"
                res += aux_word + " "
            else:
                res += word + " "
        self.resolutions.append(res.strip())
        return res

    def get_insult_list(self, server):
        server = Pyro4.Proxy(server)
        insult_list = server.get_insults()
        return insult_list
    
daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('insult.service')
insult_filter = InsultFilter(uri)
filter = daemon.register(insult_filter)
ns.register('insult.filter', filter)
print(f"Server uri {uri}")
print(f"Filter uri {filter}")
daemon.requestLoop()