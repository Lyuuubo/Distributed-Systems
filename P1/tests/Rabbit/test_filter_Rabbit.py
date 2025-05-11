import unittest
import pika
import redis
import time
from collections import Counter

# We need active:
# - InsultFilter.py
# or
# - InsultFilter.py (2 or more)
class TestFilterRabbit(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Connect to Redis
        # self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        # self.redis_queue = "result_queue"

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.queue = 'insult_filter_queue'
        self.response_queue = 'response_filter_queue'

        # Declare a queue
        self.channel.queue_declare(queue=self.queue)
        self.channel.queue_declare(queue=self.response_queue)

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
            # self.channel.basic_publish(exchange='', routing_key=self.queue, body=msg)
            self.channel.basic_publish(exchange='', 
                            routing_key=self.queue, 
                            properties=pika.BasicProperties(reply_to=self.response_queue),
                            body=msg)
        time.sleep(1)
        result = []
        while True:
            method_frame, header_frame, body = self.channel.basic_get(queue=self.response_queue, auto_ack=True)
            if method_frame:
                result.append(body.decode())
            else: break
        assert Counter(result) == Counter(self.result)

if __name__ == '__main__':
    unittest.main()