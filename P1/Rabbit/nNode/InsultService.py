import pika
import multiprocessing
import random
import time
import redis

def storeInsult(insult):
    insults = client_redis.lrange(insult_list, 0, -1)
    if insult not in insults:
        # insult_list.append(insult)
        client_redis.lpush(insult_list, insult)
        print(f"Save insult: {insult}")
    else:
        print(f"Insult ({insult}) is already in the list")

def getInsult(ch, method, properties, body):
    insults = client_redis.lrange(insult_list, 0, -1)
    response = random.choice(insults)
    print(f"Sent {response}")
    
    # Return response to client
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        body=str(response),
    )

def startBroadcast():
    channel.basic_publish(exchange='', routing_key='broadcast_queue', body='start')

def stopBroadcast():
    channel.basic_publish(exchange='', routing_key='broadcast_queue', body='stop')
    

# Define the callback function
def callback(ch, method, properties, body):
    value = body.decode()
    print(f" [x] Received {value}")
    if value == 'X1':
        getInsult(ch, method, properties, body)
    elif value == 'X2':
        startBroadcast()
    elif value == 'X3':
        stopBroadcast()
    else:
        storeInsult(value)

if __name__ == "__main__":
    insult_list = "insult_list"
    broadcast_active = None

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    client_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # Declare a queue (ensure it exists)
    channel.queue_declare(queue='request_queue')

    # Declare a queue
    channel.queue_declare(queue='broadcast_queue')

    # Consume messages
    channel.basic_consume(queue='request_queue', on_message_callback=callback, auto_ack=True)

    print("Consumer")
    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()