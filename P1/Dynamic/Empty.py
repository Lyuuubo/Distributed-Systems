import pika
import redis
import time

# Code to empy the rabbit queue used in Dynamic Scaling
if __name__ == "__main__":

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    work_queue = 'work_queue_v1'
    count_queue = 'count_queue_v1'

    # Declare new rabbit queue
    channel.queue_purge(queue=work_queue)
    channel.queue_purge(queue=count_queue)

    print('FIN')