import pika
import redis

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Declare a queue (ensure it exists)
channel.queue_declare(queue='insult')

# Define the callback function
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    insults = client.lrange("insult_list", 0, -1)
    if body.decode() not in insults:
        client.lpush("insult_list", body.decode())


# Consume messages
channel.basic_consume(queue='insult', on_message_callback=callback, auto_ack=True)

print("Consumer")
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
