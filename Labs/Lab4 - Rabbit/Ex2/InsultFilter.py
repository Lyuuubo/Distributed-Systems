import pika
import redis

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Declare a queue (ensure it exists)
channel.queue_declare(queue='text_chanel')
resultList = "result_list"
insults = ["tonto","perro","feo","gordo","cavero"]

# Define the callback function
def callback(ch, method, properties, body):
    text = body.decode()
    for insult in insults:
            if insult in text:
                text = text.replace(insult, "CENSORED")
                break
    print(f" [x] Received {text}")
    client.lpush(resultList, text)

# Consume messages
channel.basic_consume(queue='text_chanel', on_message_callback=callback, auto_ack=True)

print("Consumer")
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()