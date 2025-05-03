import unittest
import xmlrpc.client
from collections import Counter

# We need active (active in order):
# - nNode/MasterService.py
# - nNode/InsultFilter.py (1 or more)
class TestFilterXMLRPC(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.messages = [
            'hola tonto','que tal','com estas','que feo ets deu meu',
                'dema a jugar a futbol gordo','fes el treball inutil'
        ]
        self.result = [
            'hola CENSORED','que tal','com estas','que CENSORED ets deu meu',
            'dema a jugar a futbol CENSORED','fes el treball CENSORED'
        ]
        self.service = xmlrpc.client.ServerProxy('http://localhost:8000')

    def test_1_produce_work(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        for msg in self.messages:
            response = node.produce_work(msg)
            assert response == f"Produce work: {msg}"

    def test_2_see_work_queue(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.obtain_work_queue()
        assert Counter(response) == Counter(self.messages)

    def test_3_consume_work(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        for msg,res in zip(self.messages,self.result):
            response = node.consume_work()
            assert response ==  f'Consume work: {msg} -> {res}'
    
    def test_4_not_work(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.consume_work()
        assert response == 'Any work in the queue'

    def test_5_see_result_queue(self):
        url = self.service.connect_to_node()
        node = xmlrpc.client.ServerProxy(url)
        response = node.obtain_result_queue()
        assert Counter(response) == Counter(self.result)

    @classmethod
    def tearDownClass(self):
        self.service.reset()

if __name__ == '__main__':
    unittest.main()