import unittest
import time
import random
import xmlrpc.client

class TestServiceXMLRPC(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.insults = ['Tonto','Perro','Feo','Rata']
        self.service = xmlrpc.client.ServerProxy('http://localhost:8200')
        self.subscribers = ['http://localhost:8201','http://localhost:8202','http://localhost:8203','http://localhost:8204']

    def test_1_add_insult(self):
        for insult in self.insults:
            response = self.service.send_insult(insult)
            assert response == f'{insult} ADDED'
        insult = random.choice(self.insults)
        response = self.service.send_insult(insult)
        assert response == f'{insult} EXIST'

    def test_2_get_insults(self):
        response = self.service.get_insults()
        assert response == self.insults

    def test_3_insult_me(self):
        response = self.service.insult_me()
        assert response in self.insults

    def test_4_remove_insult(self):
        insult = random.choice(self.insults)
        response = self.service.remove_insult(insult)
        assert response == f'{insult} REMOVED'
        response = self.service.remove_insult(insult)
        assert response == f'{insult} NOT EXIST'

    def test_5_add_subscriber(self):
        for sub in self.subscribers:
            response = self.service.add_subscriber(sub)
            assert response == f'{sub} ADDED'
        sub = random.choice(self.subscribers)
        response = self.service.add_subscriber(sub)
        assert response == f'{sub} EXIST'

    def test_6_remove_subscriber(self):
        sub = 'http://localhost:8204'
        response = self.service.remove_subscriber(sub)
        assert response == f'{sub} REMOVED'
        response = self.service.remove_subscriber(sub)
        assert response == f'{sub} NOT EXIST'

    def test_7_notify_subscriber(self):
        response = self.service.notify_subscribers()
        assert response == 'Notification Actived'
        response = self.service.notify_subscribers()
        assert response == 'Notification is also Actived'
        time.sleep(8)
        response = self.service.stop_notify_subscribers()
        assert response == 'Notification Desactived'
        response = self.service.stop_notify_subscribers()
        assert response == 'Notification is also Desactived'

    @classmethod
    def tearDownClass(self):
        self.service.reset()

if __name__ == '__main__':
    unittest.main()