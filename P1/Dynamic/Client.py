import pika
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchange
channel.exchange_declare(exchange='master_queue', exchange_type='fanout')
messages = ["Hola", "Que tal", "Que passa", "Tinc gana", "Mec mec"]

print("TextProducer")
while True:
    # Publish a message
    insult = random.choice(messages)
    channel.basic_publish(exchange='master_queue', routing_key='', body=insult)
    print(f" [x] Send {insult}")
    time.sleep(0.01)

# Close connection
connection.close()