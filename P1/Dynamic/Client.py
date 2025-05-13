import pika
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchange
channel.exchange_declare(exchange='master_queue', exchange_type='fanout')
messages = "Hola tonto"

# Declare response queue
response = channel.queue_declare(queue='')
response_queue = response.method.queue

print("TextProducer")
while True:
    # Publish a message
    channel.basic_publish(exchange='master_queue', 
                          routing_key='', 
                          properties=pika.BasicProperties(reply_to=response_queue),
                          body=messages)
    #print(f" [x] Send {insult}")
    time.sleep(0.0035)

# Close connection
connection.close()