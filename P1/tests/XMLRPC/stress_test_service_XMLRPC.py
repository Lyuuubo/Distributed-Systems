import xmlrpc.client
import multiprocessing
import time
import statistics
import matplotlib.pyplot as plt
import threading

# We need active (active in order):
# - 1Node/InsultServiceLinux.py
class StressTestService:
    def __init__(self):
        # Define data needed to do the test
        self.uri = 'http://localhost:8200'
        self.number_process = 4
        self.message_process = []
        self.estimated = []
        self.requests = [1000, 2000, 5000, 10000, 20000, 50000, 100000] #[8, 16, 32]#, 64, 128]

        client = xmlrpc.client.ServerProxy(self.uri)
        print(client.send_insult("Tonto"))
        print(client.send_insult("Feo"))
        print(client.send_insult("Gordo"))

    def get_insult(self, uri, requests):
        client = xmlrpc.client.ServerProxy(uri)
        for _ in range(requests):
            client.get_insults()

    def run_test(self, num_p, request):
        print(f"Test: {num_p}:{request}")
        procs = []
        for _ in range(num_p):
            p = multiprocessing.Process(target=self.get_insult, args=(self.uri, request,))
            procs.append(p)
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
        for request in self.requests:
            self.run_test(self.number_process, request)
        client = xmlrpc.client.ServerProxy(self.uri)
        client.reset()

if __name__ == '__main__':
    test = StressTestService()
    test.do_tests()

    plt.figure(figsize=(8, 4))
    plt.plot(test.number_process, test.estimated, 'r-', label='Estimated')
    plt.plot(test.number_process, test.message_process, 'b-', label='Real')
    plt.xlabel('Clients')
    plt.ylabel('Messages')
    plt.title('Stress Test XMLRPC')
    plt.legend()
    plt.grid(True)
    plt.show()