import pika
import time
import math
import redis
import subprocess
from pathlib import Path

class Master:
    def __init__(self, work_queue, count_queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()

        # Declare exchange
        self.channel.exchange_declare(exchange='master_queue', exchange_type='fanout')

        # Declare queues
        self.channel.queue_declare(queue=work_queue)
        self.channel.queue_declare(queue=count_queue)

        # Bind the queue to the exchange
        self.channel.queue_bind(exchange='master_queue', queue=work_queue)
        self.channel.queue_bind(exchange='master_queue', queue=count_queue)

        self.work = work_queue        # Rabbit queues
        self.count = count_queue
        self.C = 1000        # Parameters to calculate the numbers of workers needed
        self.T = 2
        self.num_workers = 0    # Number and id of the workers started
        self.id_workers = []
        self.path_worker = Path(__file__).parent / 'InsultFilter.py'
        # Pick date to do graphics
        self.result_rate = []
        self.result_workers = []

    def obtain_num_workers(self):
        # Obtain publish rate
        q1 = self.channel.queue_declare(queue=self.count, passive=True)
        time.sleep(2)
        q2 = self.channel.queue_declare(queue=self.count, passive=True)
        rate = q2.method.message_count - q1.method.message_count

        # Obtain the number of events in the queue
        q1 = self.channel.queue_declare(queue=self.work, passive=True)
        count = q1.method.message_count
        print(f'\n*Rate: {rate}\t*Queue: {count}\t*Consumer : {self.C}')
        num_workers = math.ceil((count+(rate*self.T))/self.C)

        self.result_rate.append(rate)
        self.result_workers.append(num_workers)
        return num_workers
    
    def up_down_workers(self, workers_need, num_max):
        # Up workers
        if workers_need > self.num_workers:
            print(" [!] Up Workers")
            for _ in range(workers_need-self.num_workers):
                # Start new worker
                if self.num_workers <= num_max:
                    proc = subprocess.Popen(["python", self.path_worker],
                                            stdout = subprocess.DEVNULL)
                    self.id_workers.append(proc)
                    self.num_workers = self.num_workers + 1 
                    print(" -> + worker")
                else: 
                    print(f" [!] Limit workers: {num_max}")
                    break
        # Down workers
        else:
            print(" [!] Down Workers")
            for _ in range(self.num_workers-workers_need):
                # Kill first worker we started
                proc = self.id_workers.pop(0)
                proc.terminate()
                proc.wait()
                self.num_workers = self.num_workers - 1 
                print(" -> - worker")
        
    def start_managing(self, num_max):
        print(" [*] Start working :)")
        while True:
            workers_need = self.obtain_num_workers()
            print(f'Workers need: {workers_need} - Working: {self.num_workers}')
            # Balance num of workers
            if workers_need != self.num_workers:
                self.up_down_workers(workers_need, num_max)

    def start_managing_test(self, num_max, it):
        print(" [*] Start working :)")
        for _ in range(int(it/2)):
            workers_need = self.obtain_num_workers()
            print(f'Workers need: {workers_need} - Working: {self.num_workers}')
            # Balance num of workers
            if workers_need != self.num_workers:
                self.up_down_workers(workers_need, num_max)
        print(" [*] Fin Test")