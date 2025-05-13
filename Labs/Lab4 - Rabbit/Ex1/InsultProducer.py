import pika
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='insult')
insults = ["Tonto", "Perro", "Cap d'espinaca", "Gordo", "Feo","Cavero"]

print("Producer")
while True:
    # Publish a message
    insult = random.choice(insults)
    channel.basic_publish(exchange='', routing_key='insult', body=insult)
    print(f" [x] Sent {insult}")
    time.sleep(5)

# Close connection
connection.close()