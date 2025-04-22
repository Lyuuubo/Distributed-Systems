import pika
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='queue_prova')

time.sleep(2)
print("Start produce")
i = 0
while True:
    print(f"Produce message {i}")
    channel.basic_publish(exchange='', routing_key='queue_prova', body=f"Hola {i}")
    time.sleep(1)
    i = i+1