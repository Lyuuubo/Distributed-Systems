import pika
import redis
import multiprocessing
import lithops
import time
import subprocess

class StreamFuction():
    def __init__(self):
        self.list = []

    def consume_work(self, num, function, queue):
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        def callback(ch, method, properties, body):
            message = body.decode()
            self.list.append(message)
            print(f"Do something: {message}")
            # if len(self.list) >= 10:
            #     red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            #     red.lpush("prova_ff", message)

            #     with lithops.FunctionExecutor() as funct:
            #         futures = funct.map(function, self.list)
            #         print(f'Return value: {futures.get_result()}')
            #     self.list = []

        # Consume messages
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(f"Consumer {num}")
        print(' [*] Waiting for messages. To exit, press CTRL+C')
        channel.start_consuming()

    def consultNumWorkers(self, queue):
        return 1

    def stream(self, function, maxfunc, queue):
        self.consume_work("1", function, queue)
        # proc = []
        # for i in range(maxfunc):
        #     p = multiprocessing.Process(target=self.consume_work, args=("1", function, queue,))
        #     proc.append(p)
        #     p.start()

        # time.sleep(100)
        # for pr in proc:
        #     pr.terminate()
        #     pr.join()
        
        # while True:
        #     n = consultNumWorkers(queue)
        #     workers = activeProc.count()
        #     if n != workers:
        #         dif = workers - n

def return_value(message):
    return message

if __name__ == "__main__":
    lith = StreamFuction()
    lith.stream(return_value, 1, "queue_prova")