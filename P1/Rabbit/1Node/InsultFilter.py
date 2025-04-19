import pika
import redis

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

redis_queue = 'result_queue'
queue_name = 'insult_filter_queue'

# Declare neu rabbit queue
channel.queue_declare(queue=queue_name)

insults = ['tonto', 'inutil', "cap d'espicana", 'cavero', 'gordo', 'feo', 'perro']

def callback(ch, method, properties, body):
    text = body.decode()
    for insult in insults:
            if insult in text:
                text = text.replace(insult, "CENSORED")
                break
    print(f" [x] Received {text}")
    client.lpush(redis_queue, text)

# Consume messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Consumer")
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()