import unittest
import time
import random
import Pyro4
from collections import Counter

# We need active:
# - ActiceServer.py
# - InsultClient.py
# - Dynamic/InsultMaster.py
# - Dynamic/InsultSlaveService.py (1 or more)
class TestServicePyro(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # We initialize a insult list to realize the test
        self.insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]

        # We select the master name server to do the testing
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup('master.service')
        self.server = Pyro4.Proxy(uri)

    def test_1_add_insult(self):
        for insult in self.insults:
            url = self.server.get_resolver_slave()
            ns = Pyro4.locateNS(host='localhost', port=9090)
            uri = ns.lookup(url)
            slave = Pyro4.Proxy(uri)
            response = slave.add_insult(insult)
            assert response == f"Adding new insult {insult}"
        insult = random.choice(self.insults)
        response = slave.add_insult(insult)
        assert response == f"The {insult} is already stored"

    def test_2_get_insults(self):
        url = self.server.get_resolver_slave()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        response = slave.get_insults()
        assert Counter(response) == Counter(self.insults)

    def test_3_insult_me(self):
        url = self.server.get_resolver_slave()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        response = slave.random_choice()
        assert response in self.insults

    def test_4_add_subscriber(self):
        url = self.server.get_resolver_slave()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        client = ns.lookup("insult.client")
        response = slave.add_subscriber(client)
        assert response == f"Adding new subscriber {client}"
        response = slave.add_subscriber(client)
        assert response == f"The subscriber {client} is already stored"
    
    def test_5_remove_subscriber(self):
        url = self.server.get_resolver_slave()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        client = ns.lookup("insult.client")
        response = slave.remove_subscriber(client)
        assert response == f"Removing subscriber {client}"
        response = slave.remove_subscriber(client)
        assert response == f"The subscriber {client} is already removed"

    def test_6_notify_subscriber(self):
        url = self.server.get_resolver_slave()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        client = ns.lookup("insult.client")
        slave.add_subscriber(client)
        response = slave.start_broadcast()
        assert response == "Starting broadcast"
        response = slave.start_broadcast()
        assert response == "Broadcast is already started"
        time.sleep(8)
        response = slave.kill_broadcast()
        assert response == "Finishing broadcast"
        response = slave.kill_broadcast()
        assert response == "Broadcast function its already dead"

    @classmethod
    def tearDownClass(self):
        url = self.server.get_resolver_slave()
        ns = Pyro4.locateNS(host='localhost', port=9090)
        uri = ns.lookup(url)
        slave = Pyro4.Proxy(uri)
        slave.clean_insults()
        slave.clean_subscribers()

if __name__ == '__main__':
    unittest.main()