import unittest
import pika
import random
import time

class TestServiceRabbit(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.queue = 'request_queue'

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
        message = 'X4'      # Get all insults
        self.channel.basic_publish(exchange='', 
                            routing_key=self.queue, 
                            properties=pika.BasicProperties(reply_to=self.response_queue),
                            body=message)
        time.sleep(1)
        method_frame, header_frame, body = self.channel.basic_get(queue=self.response_queue, auto_ack=True)
        if method_frame:
            assert body.decode() == f"{self.insults}"
        else: assert False

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

if __name__ == '__main__':
    unittest.main()