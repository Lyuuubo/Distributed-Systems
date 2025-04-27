import unittest
import xmlrpc.client

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
        self.service = xmlrpc.client.ServerProxy('http://localhost:8300')

    def test_1_produce_work(self):
        for msg in self.messages:
            response = self.service.produce_work(msg)
            assert response == f"Produce work: {msg}"

    def test_2_see_work_queue(self):
        response = self.service.obtain_work_queue()
        assert response == self.messages

    def test_3_consume_work(self):
        for msg,res in zip(self.messages,self.result):
            response = self.service.consume_work()
            assert response ==  f'Consume work: {msg} -> {res}'
    
    def test_4_not_work(self):
        response = self.service.consume_work()
        assert response == 'Any work in the queue'

    def test_5_see_result_queue(self):
        response = self.service.obtain_result_queue()
        assert response == self.result

    @classmethod
    def tearDownClass(self):
        self.service.reset()

if __name__ == '__main__':
    unittest.main()