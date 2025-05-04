import pika
import time
import math
import redis
import subprocess
from pathlib import Path

class Master:
    def __init__(self, work, count, channel):
        self.work = work        # Rabbit queues
        self.count = count
        self.channel = channel  # Rabbit conection
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  # Redis connection
        self.C = 100        # Parameters to calculate the numbers of workers needed
        self.T = 2
        self.num_workers = 0    # Number and id of the workers started
        self.id_workers = []
        self.path_worker = Path(__file__).parent / 'InsultFilter.py'

    def obtain_num_workers(self):
        # Obtain publish rate
        q1 = channel.queue_declare(queue=self.count, passive=True)
        time.sleep(2)
        q2 = channel.queue_declare(queue=self.count, passive=True)
        rate = q2.method.message_count - q1.method.message_count

        # Obtain event consumed by workers in 1 second
        temps = [float(x) for x in self.redis.lrange("time_queue", 0, -1)]
        temps_sum = sum(temps) 
        if len(temps) != 0 and temps_sum != 0.0:
            self.C = 1/(temps_sum/len(temps))
            self.redis.ltrim("time_queue", 1, 0)

        # Obtain the number of events in the queue
        q1 = channel.queue_declare(queue=self.work, passive=True)
        count = q1.method.message_count
        print(f'\n*Rate: {rate}\t*Queue: {count}\t*Consumer : {self.C}')
        return math.ceil((count+(rate*self.T))/self.C)
    
    def up_down_workers(self, workers_need):
        # Up workers
        if workers_need > self.num_workers:
            print(" [!] Up Workers")
            for _ in range(workers_need-self.num_workers):
                # Start new worker
                proc = subprocess.Popen(["python", self.path_worker],
                                        stdout = subprocess.DEVNULL)
                self.id_workers.append(proc)
                self.num_workers = self.num_workers + 1 
                print(" -> + worker")
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
        

    def start_managing(self):
        print(" [*] Start working :)")
        while True:
            workers_need = self.obtain_num_workers()
            print(f'Workers need: {workers_need} - Working: {self.num_workers}')
            if workers_need != self.num_workers:
                self.up_down_workers(workers_need)

if __name__ == "__main__":
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    work_queue = 'work_queue_v1'
    count_queue = 'count_queue_v1'

    # Declare exchange
    channel.exchange_declare(exchange='master_queue', exchange_type='fanout')

    # Declare queues
    channel.queue_declare(queue=work_queue)
    channel.queue_declare(queue=count_queue)

    # Bind the queue to the exchange
    channel.queue_bind(exchange='master_queue', queue=work_queue)
    channel.queue_bind(exchange='master_queue', queue=count_queue)

    master = Master(work_queue, count_queue, channel)
    master.start_managing()