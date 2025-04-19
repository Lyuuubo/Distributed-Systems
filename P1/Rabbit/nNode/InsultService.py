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

def notify(list):
    print(f"Notify subscribers...")
    client_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    insults = client_redis.lrange('insult_list', 0, -1)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    while True:
        insult = random.choice(insults)
        channel.basic_publish(exchange='notify_subs', routing_key='', body=insult)
        print(f" [x] Sent '{insult}'")
        time.sleep(5)

def startBroadcast():
    global broadcast_active
    if broadcast_active is None:
        broadcast_active = multiprocessing.Process(target=notify, args=(insult_list,))
        broadcast_active.start()
        print ("Broadcast Actived")
    else:
        print ("Broadcast is also Actived")

def stopBroadcast():
    global broadcast_active
    if broadcast_active is not None:
        broadcast_active.terminate()
        broadcast_active.join()
        broadcast_active = None
        print ("Broadcast Desactived")
    else:
        print ("Broadcast is also Desactived")

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

    # Declare a fanout exchange
    channel.exchange_declare(exchange='notify_subs', exchange_type='fanout')

    # Consume messages
    channel.basic_consume(queue='request_queue', on_message_callback=callback, auto_ack=True)

    print("Consumer")
    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()