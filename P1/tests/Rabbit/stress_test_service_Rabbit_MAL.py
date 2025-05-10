import pika
import multiprocessing
import time
import random
import statistics
import matplotlib.pyplot as plt
import requests
from requests.auth import HTTPBasicAuth

# We need active (active in order):
# - 1Node/InsultFilterTT.py
class StressTestService:
    def __init__(self):
        self.number_process = 4
        self.publish_rate = []
        self.consumer_rate = []
        self.time_stamp = []
        self.requests = 1048576 #[1048576]#, 20000, 50000, 100000, 200000, 500000]
        self.insults= ['Perro','Tonto','Inutil','Feo','Gordo']

    def send_insult(self, requests):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Declare a queue
        channel.queue_declare(queue='insult_filter_queue')

        # Declare response queue
        response = channel.queue_declare(queue='', exclusive=True)
        response_queue = response.method.queue

        for _ in range(requests):
            channel.basic_publish(exchange='', 
                                routing_key='insult_filter_queue', 
                                properties=pika.BasicProperties(reply_to=response_queue),
                                body='A')
        connection.close()

    def run_test(self, request):
        print(f"Test-> {request}")
        procs = []
        rq = int(request / self.number_process)
        for _ in range(self.number_process):
            p = multiprocessing.Process(target=self.send_insult, args=(rq,))
            procs.append(p)
        start = time.time()
        for proc in procs:
            proc.start()

        ini = time.time()
        # self.publish_rate.append(0)
        self.consumer_rate.append(0)
        self.time_stamp.append(0)
        url = f'http://localhost:15672/api/queues/%2f/insult_filter_queue'
        publish_rate = 1
        consumer_rate = 0
        while publish_rate != 0 or consumer_rate != 0:
            time.sleep(10)
            response = requests.get(url, auth=HTTPBasicAuth('guest', 'guest'))
            data = response.json()
            # print(data)
            publish_rate = data['message_stats']['publish_details']['rate']
            consumer_rate = data['message_stats']['deliver_get_details']['rate']
            self.publish_rate.append(publish_rate)
            self.consumer_rate.append(consumer_rate)
            self.time_stamp.append(time.time()-ini)
            print(f"  Publish rate: {publish_rate}")
            print(f"  Consumer rate: {consumer_rate}")

        
        print("FIN")
        


        
        # duration = end - start
        # self.time_taken.append(duration)
        # mean_petition = duration / request

        # print(f"  Total time: {duration:.2f} s")
        # print(f"  Mean time for petition: {mean_petition:.8f} s")
        # print(f"  Message process /s: {1/mean_petition:.8f}")
        # print("-" * 40)

    def do_tests(self):
        #for request in self.requests:
        self.run_test(self.requests)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_purge(queue='insult_filter_queue')

if __name__ == '__main__':
    test = StressTestService()
    test.do_tests()

    plt.figure(figsize=(8, 4))
    plt.plot(test.time_stamp, test.publish_rate, 'r-', label='Publicación')
    plt.plot(test.time_stamp, test.consumer_rate, 'b-', label='Entrega')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Mensajes')
    plt.legend()
    plt.grid(True)
    plt.show()

