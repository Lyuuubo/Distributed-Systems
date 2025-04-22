import pika
import multiprocessing
import lithops

def consume_work(num, function, queue):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        message = body.decode()
        print(f"Do something: {body.decode()}")

        with lithops.FunctionExecutor() as funct:
            futures = funct.map(function, message)
            print(f'Return value: {futures.get_result()}')

    # Consume messages
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(f"Consumer {num}")
    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()

def consultNumWorkers(queue):
    return 1

def stream(function, maxfunc, queue):
    consume_work("1", function, queue)
    # activeProc = []
    # while True:
    #     n = consultNumWorkers(queue)
    #     workers = activeProc.count()
    #     if n != workers:
    #         dif = workers - n

def return_value(message):
    return message

if __name__ == "__main__":
    stream(return_value, 10, "queue_prova")