import unittest
import pika
import redis
import time

class TestFilterRabbit(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Connect to Redis
        self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.redis_queue = "result_queue"

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.queue = 'insult_filter_queue'

        # Declare a queue
        self.channel.queue_declare(queue=self.queue)

        self.messages = [
            'hola tonto','que tal','com estas','que feo ets deu meu',
                'dema a jugar a futbol gordo','fes el treball inutil'
        ]
        self.result = [
            'fes el treball CENSORED','dema a jugar a futbol CENSORED',
            'que CENSORED ets deu meu','com estas','que tal','hola CENSORED'
        ]

    def test_produce_work(self):
        for msg in self.messages:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=msg)
        time.sleep(0.5)
        result = self.client.lrange(self.redis_queue, 0, -1)
        print(result)
        assert result == self.result
                
    @classmethod
    def tearDownClass(self):
        self.client.ltrim(self.redis_queue, 1, 0)

if __name__ == '__main__':
    unittest.main()