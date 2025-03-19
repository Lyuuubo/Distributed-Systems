import pika
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='text_chanel')
messages = ["Hola", "Que tal", "Que passa", "Tinc gana", "Mec mec"]

print("TextProducer")
while True:
    # Publish a message
    insult = random.choice(messages)
    channel.basic_publish(exchange='', routing_key='text_chanel', body=insult)
    print(f" [x] Sent {insult}")
    time.sleep(5)

# Close connection
connection.close()