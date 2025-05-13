import pika
import multiprocessing
import time
import matplotlib.pyplot as plt
import threading

# We need active (active in order):
# - Rabbit/InsultFilter.py
class StressTestService:
    def __init__(self):
        self.number_process = 4
        self.consumer_rate = []
        self.time_stamp = []
        self.requests = [1000, 2000, 5000, 10000, 20000, 50000, 100000]

    def send_insult(self, requests, i):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Declare a queue
        channel.queue_declare(queue='insult_filter_queue')

        # Declare response queue
        response = channel.queue_declare(queue='')
        response_queue = response.method.queue

        for _ in range(requests):
            channel.basic_publish(exchange='', 
                                routing_key='insult_filter_queue', 
                                properties=pika.BasicProperties(reply_to=response_queue),
                                body='A')
        count = 0
        while True:
            method_frame, header_frame, body = channel.basic_get(queue=response_queue, auto_ack=True)
            if method_frame:
                count += 1
            if count >= requests: break
            #print(self.count)
        connection.close()

    def run_test(self, request):
        print(f"Test-> {request}")
        procs = []
        i = 0
        for _ in range(self.number_process):
            p = multiprocessing.Process(target=self.send_insult, args=(request,i))
            procs.append(p)
            i+= 1
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
    total_requests = [req * test.number_process for req in test.requests]
    plt.plot(total_requests, test.consumer_rate, 'b-', label='MessagesConsumed/s')
    plt.xlabel('Total Requests')
    plt.ylabel('Consumed/s')
    plt.title('Stress Test RabbitMQ')
    plt.legend()
    plt.grid(True)
    plt.show()

