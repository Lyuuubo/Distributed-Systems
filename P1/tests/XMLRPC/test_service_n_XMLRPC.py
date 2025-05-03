import unittest
import time
import random
import xmlrpc.client
from collections import Counter

# We need active (active in order):
# - nNode/MasterService.py
# - nNode/SlaveService (1 or more)
# - nNode/BroadcastService
# - nNode/s1.py (s2 and s3 also)
class TestServiceXMLRPC(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.insults = ['Tonto','Perro','Feo','Rata']
        self.service = xmlrpc.client.ServerProxy('http://localhost:8000')   # Connect to master
        self.subscribers = ['http://localhost:8101','http://localhost:8102','http://localhost:8103']

    def test_1_add_insult(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        for insult in self.insults:
            response = node.send_insult(insult)
            assert response == f'{insult} ADDED'
        insult = random.choice(self.insults)
        response = node.send_insult(insult)
        assert response == f'{insult} EXIST'

    def test_2_get_insults(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.get_insults()
        assert Counter(response) == Counter(self.insults)

    def test_3_insult_me(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.insult_me()
        assert response in self.insults

    def test_4_add_subscriber(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        for sub in self.subscribers:
            response = node.add_subscriber(sub)
            assert response == f'{sub} ADDED'
        sub = random.choice(self.subscribers)
        response = node.add_subscriber(sub)
        assert response == f'{sub} EXIST'

    def test_5_notify_subscriber(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.notify_subscribers()
        assert response == 'Notification Actived'
        response = node.notify_subscribers()
        assert response == 'Notification is also Actived'
        time.sleep(8)
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.stop_notify_subscribers()
        assert response == 'Notification Desactived'
        response = node.stop_notify_subscribers()
        assert response == 'Notification is also Desactived'

    @classmethod
    def tearDownClass(self):
        self.service.reset()

if __name__ == '__main__':
    unittest.main()