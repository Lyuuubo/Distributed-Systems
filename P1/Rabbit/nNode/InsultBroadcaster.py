import pika
import multiprocessing
import redis
import random
import time

def notify():
    print(f"Notify subscribers...")
    insults = ['tonto', 'inutil', "cap d'espicana", 'cavero', 'gordo', 'feo', 'perro']
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
        broadcast_active = multiprocessing.Process(target=notify)
        broadcast_active.start()
        print(" [*] Start Broadcast")
    else:
        print (" - Broadcast is also Actived")

def stopBroadcast():
    global broadcast_active
    if broadcast_active is not None:
        broadcast_active.terminate()
        broadcast_active.join()
        broadcast_active = None
        print(" [*] Stop Broadcast")
    else:
        print (" - Broadcast is also Desactived")

def callback(ch, method, properties, body):
    value = body.decode()
    print(f" [x] Received {value}")
    if value == 'start':
        startBroadcast()
    elif value == 'stop':
        stopBroadcast()

if __name__ == "__main__":
    broadcast_active = None

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare("broadcast_queue")

    # Declare a fanout exchange
    channel.exchange_declare(exchange='notify_subs', exchange_type='fanout')

    channel.basic_consume(queue="broadcast_queue", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting")
    channel.start_consuming()