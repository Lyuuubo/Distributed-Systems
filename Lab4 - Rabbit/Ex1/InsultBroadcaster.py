import pika
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')
insults = ["Tonto", "Perro", "Cap d'espinaca", "Gordo", "Feo","Cavero"]

print("Publisher")

# Publish a message
while True:
    insult = random.choice(insults)
    channel.basic_publish(exchange='logs', routing_key='', body=insult)
    print(f" [x] Sent '{insult}'")
    time.sleep(5)

# Close connection
connection.close()