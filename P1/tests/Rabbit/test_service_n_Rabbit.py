import unittest
import pika
import random
import time
import redis

# We need active:
# - nNode/InsultService.py
# - nNode/InsultBroadcaster.py
# - nNode/Subscriber.py (1 or more)
class TestServiceRabbit(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Connect to Redis
        self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.redis_queue = "insult_list"

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.queue = 'request_queue_n'

        # Declare a queue
        self.channel.queue_declare(queue=self.queue)

        # Declare response queue
        response = self.channel.queue_declare(queue='', exclusive=True)
        self.response_queue = response.method.queue

        self.insults= ['Perro','Tonto','Inutil','Feo','Gordo']

    def test_1_store_insult(self):
        for insult in self.insults:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=insult)
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=random.choice(self.insults))

    def test_2_obtain_insult_list(self):
        insults = self.client.lrange(self.redis_queue, 0, -1)
        for insult in insults:
            assert insult in self.insults

    def test_3_get_insult(self):
        message = 'X1'      # Get random insult
        self.channel.basic_publish(exchange='', 
                            routing_key=self.queue, 
                            properties=pika.BasicProperties(reply_to=self.response_queue),
                            body=message)
        time.sleep(1)
        method_frame, header_frame, body = self.channel.basic_get(queue=self.response_queue, auto_ack=True)
        if method_frame:
            assert body.decode() in self.insults
        else: assert False

    def test_4_braodcast(self):
        message = "X2"      # Start broadcast
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)   # Reply the message
        time.sleep(10)
        message = "X3"      # Stop broadcast
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)   # Reply the message
    
    @classmethod
    def tearDownClass(self):
        self.client.ltrim(self.redis_queue, 1, 0)

if __name__ == '__main__':
    unittest.main()