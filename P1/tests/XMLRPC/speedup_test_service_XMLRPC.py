import xmlrpc.client
import multiprocessing
import time
import matplotlib.pyplot as plt
from collections import deque
from pathlib import Path

# We need active (active in order):
# - XMLRPC/1Node/InsultServiceLinux.py (3 terminals)
class StressTestService:
    def __init__(self):
        # Define data needed to do the test
        print("Prepare environment")
        self.uri = deque(['http://localhost:8002','http://localhost:8003','http://localhost:8004'])

        self.number_process = 4
        self.message_process = []
        self.requests = 100000

        for uri in list(self.uri):
            client = xmlrpc.client.ServerProxy(uri)
            print(client.send_insult("Tonto"))
            print(client.send_insult("Feo"))
            print(client.send_insult("Gordo"))

    def get_insult(self, requests, servers):
        for _ in range(requests):
            uri = servers.popleft()
            client = xmlrpc.client.ServerProxy(uri)
            client.insult_me()
            servers.append(uri)

    def run_test(self, num_p, request, num_servers):
        print(f"Test-> {num_servers+1} servers: {request} requests")
        procs = []
        if num_servers == 0:
            list_server = deque([self.uri[0]])
        elif num_servers == 1:
            list_server = deque([self.uri[0], self.uri[1]])
        else:
            list_server = self.uri

        for _ in range(num_p):
            p = multiprocessing.Process(target=self.get_insult, args=(request,list_server,))
            procs.append(p)
            list_server.append(list_server.popleft())
        start = time.time()
        for proc in procs:
            proc.start()
        for proc in procs:
            proc.join()
        end = time.time()
        
        duration = end - start
        mean_petition = (request * num_p) / duration

        print(f"  Total time: {duration:.2f} s")
        print(f"  Message process /s: {mean_petition:.4f} s")
        self.message_process.append(mean_petition)
        print("-" * 40)

    def do_tests(self):
        for servers in range(3):
            self.run_test(self.number_process, self.requests, servers)
        # for uri in list(self.uri):
        #     client = xmlrpc.client.ServerProxy(uri)
        #     client.reset()

if __name__ == '__main__':
    test = StressTestService()
    test.do_tests()

    plt.figure(figsize=(8, 4))
    num_servers = [1,2,3]
    plt.plot(num_servers, num_servers, 'r-o', label='Estimated')
    speed_up = [val/test.message_process[0] for val in test.message_process]
    #plt.plot(num_servers, test.message_process, 'b-', label='Real')
    plt.plot(num_servers, speed_up, 'b-o', label='Real')
    plt.xlabel('Servers')
    plt.ylabel('Speedup')
    plt.legend()
    plt.grid(True)
    plt.title("SpeedUp XMLRPC")
    plt.show()