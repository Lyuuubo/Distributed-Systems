import unittest
import time
import random
import Pyro4
from collections import Counter

# We need active:
# - ActiceServer.py
# - InsultClient.py
# - Static/InsultService.py

class TestServicePyro(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        # We initialize a insult list to realize the test
        self.insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]

        # We select the name server to do the testing
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('insult.service')
        self.server = Pyro4.Proxy(uri)

    def test_1_add_insult(self):
        for insult in self.insults:
            response = self.server.add_insults(insult)
            assert response == f"Added insult: {insult}"
        insult = random.choice(self.insults)
        response = self.server.add_insults(insult)
        assert response == f"{insult} already exists"

    def test_2_get_insults(self):
        response = self.server.get_insults()
        assert Counter(response) == Counter (self.insults)

    def test_3_insult_me(self):
        response = self.server.random_insult()
        assert response in self.insults

    def test_4_remove_insult(self):
        insult = random.choice(self.insults)
        response = self.server.remove_insult(insult)
        assert response == f"Removed insult: {insult}"
        response = self.server.remove_insult(insult)
        assert response == f"{insult} not registered"

    def test_5_add_subscriber(self):
        client = "insult.client"
        response = self.server.add_subscriber(client)
        assert response == f"New subscriber {client}"
        response = self.server.add_subscriber(client)
        assert response == f"Subscriber already added: {client}"

    def test_6_remove_subscriber(self):
        client = "insult.client"
        response = self.server.remove_subscriber(client)
        assert response == f"Removed subscriber {client}"
        response = self.server.remove_subscriber(client)
        assert response == f"Subscriber already removed: {client}"

    def test_7_notify_subscriber(self):
        self.server.add_insults(random.choice(self.insults))
        client = "insult.client"
        self.server.add_subscriber(client)
        response = self.server.random_events()
        assert response == "random events activated"
        response = self.server.random_events()
        assert response == "already running"
        time.sleep(8)
        response = self.server.kill_random_events()
        assert response == "random events stopped"
        response = self.server.kill_random_events()
        assert response == "no thread running"

if __name__ == '__main__':
    unittest.main()