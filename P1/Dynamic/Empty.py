import pika
import redis
import time

if __name__ == "__main__":

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'count_queue_v1'

    # Declare exchange
    channel.exchange_declare(exchange='master_queue', exchange_type='fanout')

    # Declare new rabbit queue
    channel.queue_declare(queue=queue_name)
    
    # Bind the queue to the exchange
    channel.queue_bind(exchange='master_queue', queue=queue_name)

    def callback(ch, method, properties, body):
        print(body.decode())

    # Consume messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Consumer")
    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()