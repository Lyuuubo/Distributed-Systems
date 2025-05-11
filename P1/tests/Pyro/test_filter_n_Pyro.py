import unittest
import Pyro4
from collections import Counter

# We need active:
# - ActiceServer.py
# - Dynamic/InsultMaster.py
# - Dynamic/InsultSlaveService.py (at least 1 to add some insults to the db)
# - Dynamic/InsultSlaveFilter.py (1 or more)

class TestFilterPyro(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # We initialize a insult list to realize the test
        self.insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]

        # We select the insult server and the filter server to do the testing
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('master.service')
        self.server = Pyro4.Proxy(uri)

        url = self.server.get_resolver_slave()
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        for insult in self.insults:
            slave.add_insult(insult)

        # We initialize some petitions with the insults above
        self.petitions = [
            "No puedo creer que fueras tan idiota como para hacer eso.",
            "Hoy hace un clima espectacular para salir a caminar.",
            "Siempre llegas tarde, eres un inútil para organizarte.",
            "Tu presentación estuvo excelente, muy bien hecha.",
            "Deja de comportarte como un tonto, por favor.",
            "La película fue larga pero bastante entretenida.",
            "Ese imbécil casi choca mi coche esta mañana.",
            "Gracias por tu ayuda con el proyecto, fue muy valiosa."
        ]

        # We initialize the resolutions to the petitions above
        self.resolutions = [
            "No puedo creer que fueras tan CENSORED como para hacer eso.",
            "Hoy hace un clima espectacular para salir a caminar.",
            "Siempre llegas tarde, eres un CENSORED para organizarte.",
            "Tu presentación estuvo excelente, muy bien hecha.",
            "Deja de comportarte como un CENSORED, por favor.",
            "La película fue larga pero bastante entretenida.",
            "Ese CENSORED casi choca mi coche esta mañana.",
            "Gracias por tu ayuda con el proyecto, fue muy valiosa."
        ]

    def test_1_produce_work(self):
         for petition in self.petitions:
            url = self.server.get_resolver_filter()
            ns = Pyro4.locateNS(host='localhost', port=9090)
            uri = ns.lookup(url)
            filter = Pyro4.Proxy(uri)
            response = filter.add_petition(petition)
            assert response == f"Adding new petition {petition}"

    def test_2_get_work(self):
        url = self.server.get_resolver_filter()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        filter = Pyro4.Proxy(uri)
        response  = filter.retrieve_petitions()
        print(Counter(response))
        print(Counter(self.petitions))
        assert Counter(response) == Counter(self.petitions)

    def test_3_get_resolutions(self):
        for resolution in self.resolutions:
            url = self.server.get_resolver_filter()
            ns = Pyro4.locateNS(host='localhost', port=9090)
            uri = ns.lookup(url)
            filter = Pyro4.Proxy(uri)
            response = filter.resolve_petition()
            assert response == f"Resolution done: {resolution}"
    
    def test_4_not_work(self):
        url = self.server.get_resolver_filter()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        filter = Pyro4.Proxy(uri)
        response = filter.resolve_petition()
        assert response == "No job to be done"

    def test_5_see_result_queue(self):
        url = self.server.get_resolver_filter()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        filter = Pyro4.Proxy(uri)
        response = filter.retrieve_resolutions()
        assert Counter(response) == Counter(self.resolutions) 

    @classmethod
    def tearDownClass(self):
            url = self.server.get_resolver_slave()
            ns = Pyro4.locateNS(host='localhost', port=9090)
            uri = ns.lookup(url)
            slave = Pyro4.Proxy(uri)
            slave.clean_insults()
            url = self.server.get_resolver_filter()
            ns = Pyro4.locateNS(host='localhost', port=9090)
            uri = ns.lookup(url)
            filter= Pyro4.Proxy(uri)
            filter.clean_petitions()
            filter.clean_resolutions()

if __name__ == '__main__':
    unittest.main()