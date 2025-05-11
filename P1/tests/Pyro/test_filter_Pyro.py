import unittest
import Pyro4
from collections import Counter

# We need active:
# - ActiceServer.py
# - Static/InsultService.py
# - Static/InsultFilter.py
class TestFilterPyro(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # We initialize a insult list to realize the test
        self.insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]

        # We select the insult server and the filter server to do the testing
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('insult.service')
        self.server = Pyro4.Proxy(uri)
        uri = ns.lookup('insult.filter')
        self.filter = Pyro4.Proxy(uri)

        # We register all insults to filter some petitions
        for insult in self.insults:
            self.server.add_insult(insult)

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
            response = self.filter.add_petition(petition)
            assert response == f"Adding new message {petition}"
        
    def test_2_get_work(self):
        response = self.filter.get_petitions()
        assert Counter(response) == Counter(self.petitions)

    def test_3_get_resolutions(self):
        for resolution in self.resolutions:
            response = self.filter.resolve_petition()
            assert response == f"Resolution done: {resolution}"

    def test_4_not_work(self):
        response = self.filter.resolve_petition()
        assert response == "No job to be done"

    def test_5_see_result_queue(self):
        response = self.filter.get_resolutions()
        assert Counter(response) == Counter(self.resolutions) 

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == '__main__':
    unittest.main()
