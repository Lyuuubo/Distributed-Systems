import pika
import multiprocessing
import time
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path
import random

# We need active (active in order):
# Any
class StressTestService:
    def __init__(self):
        self.number_process = 3
        self.consumer_rate = []
        self.filter_queues = ["filter_work1","filter_work2","filter_work3"]
        self.requests = 100000
        self.path_worker = Path(__file__).parent.parent.parent/'Rabbit'/'InsultFilter.py'

    def send_insult(self, requests, list_queues):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Declare a queue
        # channel.queue_declare(queue='insult_filter_queue')

        # Declare response queue
        response = channel.queue_declare(queue='')
        response_queue = response.method.queue

        for _ in range(requests):
            queue =  list_queues.pop(0)
            list_queues.append(queue)
            channel.basic_publish(exchange='', 
                                routing_key=queue,
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

    def run_test(self, request, num_servers):
        print(f"Test-> {num_servers+1} servers: {request} requests")
        procs = []
        if num_servers == 0:
            list_queue = [self.filter_queues[0]]
        elif num_servers == 1:
            list_queue = [self.filter_queues[0], self.filter_queues[1]]
        else:
            list_queue = self.filter_queues

        for _ in range(self.number_process):
            p = multiprocessing.Process(target=self.send_insult, args=(request, list_queue.copy(),))
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
        procs = []
        queues = list(self.filter_queues)
        for servers in range(3):
            queue = queues.pop(0)
            print(queue)
            proc = subprocess.Popen(['python3', self.path_worker, '--queue', queue]
                                    ,stdout = subprocess.DEVNULL)
            procs.append(proc)
            time.sleep(2)
            self.run_test(self.requests, servers)
        for proc in procs:
            proc.terminate()
            proc.wait()
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

if __name__ == '__main__':
    test = StressTestService()
    test.do_tests()

    plt.figure(figsize=(8, 4))
    num_servers = [1,2,3]
    plt.plot(num_servers, num_servers, 'r-o', label='Estimated')
    speed_up = [val/test.consumer_rate[0] for val in test.consumer_rate]
    #plt.plot(num_servers, test.message_process, 'b-', label='Real')
    plt.plot(num_servers, speed_up, 'b-o', label='Real')
    plt.xlabel('Servers')
    plt.ylabel('Speedup')
    plt.legend()
    plt.grid(True)
    plt.title("SpeedUp RabbitMQ")
    plt.show()