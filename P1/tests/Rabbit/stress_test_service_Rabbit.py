import pika
import multiprocessing
import time
import random
import statistics
import matplotlib.pyplot as plt
import threading

# We need active (active in order):
# - 1Node/InsultFilterTT.py
class StressTestService:
    def __init__(self):
        self.number_process = 4
        self.consumer_rate = []
        self.time_stamp = []
        self.lock = multiprocessing.Lock()
        self.count = multiprocessing.Value("i", 0)
        self.requests = [1000, 2000, 5000, 10000, 20000, 50000, 100000]#, 50000, 100000, 200000, 500000]

    def count_msg(self, response_queue, request):
        request = request * self.number_process
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        def callback(ch, method, properties, body):
            with self.lock: self.count.value += 1

        channel.basic_consume(queue=response_queue, on_message_callback=callback, auto_ack=True)
        while True:
            connection.process_data_events()
            #print(self.count)
            if self.count.value >= request: break

    def send_insult(self, requests):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Declare a queue
        channel.queue_declare(queue='insult_filter_queue')

        # Declare response queue
        response = channel.queue_declare(queue='')
        response_queue = response.method.queue

        threads = []
        for _ in range(2):
            th = threading.Thread(target=self.count_msg, args=(response_queue, requests))
            th.start()
            threads.append(th)

        for _ in range(requests):
            channel.basic_publish(exchange='', 
                                routing_key='insult_filter_queue', 
                                properties=pika.BasicProperties(reply_to=response_queue),
                                body='A')
        for thread in threads:
            thread.join()
        self.count.value = 0
        connection.close()

    def run_test(self, request):
        print(f"Test-> {request}")
        procs = []
        for _ in range(self.number_process):
            p = multiprocessing.Process(target=self.send_insult, args=(request,))
            procs.append(p)
        start = time.time()
        for proc in procs:
            proc.start()
        for proc in procs:
            proc.join()
        fin = time.time()

        all_time = fin - start
        #self.time_stamp(time)
        consum = self.number_process*request / all_time
        self.consumer_rate.append(consum)
        print(f"  Total Time: {all_time}")
        print(f"  Consumer: {consum}")

    def do_tests(self):
        for request in self.requests:
            self.run_test(request)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_purge(queue='insult_filter_queue')

if __name__ == '__main__':
    test = StressTestService()
    test.do_tests()

    plt.figure(figsize=(8, 4))
    # plt.plot(test.time_stamp, test.publish_rate, 'r-', label='Publicación')
    plt.plot(test.requests, test.consumer_rate, 'b-', label='Consumició')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Mensajes')
    plt.legend()
    plt.grid(True)
    plt.show()

