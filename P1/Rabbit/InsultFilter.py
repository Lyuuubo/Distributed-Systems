import pika
import argparse
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

parser = argparse.ArgumentParser()
parser.add_argument('--queue', type=str, help='Queue where server listenning')

args = parser.parse_args()  
if args.queue is None:
    queue_name = 'insult_filter_queue'
else:
    queue_name = args.queue

# Declare new rabbit queue
channel.queue_declare(queue=queue_name)

insults = ['tonto', 'inutil', "cap d'espicana", 'cavero', 'gordo', 'feo', 'perro']

def callback(ch, method, properties, body):
    text = body.decode()
    for insult in insults:
            if insult in text:
                text = text.replace(insult, "CENSORED")
    #print(f" [x] Received {text}")
    time.sleep(0.005)

    # Return response to client
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        body=str(text),
    )

# Consume messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(f'Consumer: {queue_name}')
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()