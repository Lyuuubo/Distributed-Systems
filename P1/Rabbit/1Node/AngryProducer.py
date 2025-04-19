import pika
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
queue_name = 'insult_filter_queue'
channel.queue_declare(queue=queue_name)
messages = ["Hola tonto", "Que tal perro", "Que passa feo", "Tinc gana gordo", "Mec mec cavero"]

print("AngryProducer")
while True:
    # Publish a message
    insult = random.choice(messages)
    channel.basic_publish(exchange='', routing_key=queue_name, body=insult)
    print(f" [x] Sent {insult}")
    time.sleep(3)

# Close connection
connection.close()