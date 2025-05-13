import redis
import time
import multiprocessing
import json
import random
from itertools import cycle
from matplotlib import pyplot as plt

# Before testing:
# - CleanIdentifier.py

# We need active:
# - InsultService.py (3 instances)

client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
service_queues = []
insult_list = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_petitions = [1000, 2000, 3000, 4000, 5000]
max_cpu = 4

def petition_queues(nodes):
    service_queues.clear()
    for i in range(nodes):
       service_queues.append("petitions_queue" + str(i + 1))

    print(service_queues)

def initialize_insults():
    client.ltrim("insult_queue", 1, 0)
    for insult in insult_list:
            petition = {
                "operation" : "X1",
                "data" : insult
            }
            client.lpush(service_queues[0], json.dumps(petition))

# We retrieve insults for all the number of petitions that the client indicates
def spam__void_petitions(number_petitions):
    service_rr = cycle(service_queues)
    petition = {
        "operation" : "X5",
        "data" : ""
    }
    for _ in range(number_petitions):
        client.lpush(next(service_rr), json.dumps(petition))
        client.incr("number_pushes")

# We define a function to do the testing
def run_tests(number_petitions, number_process):
    process = []

    start = time.time()

    for _ in range(number_process):  
        p = multiprocessing.Process(target=spam__void_petitions, args=(number_petitions,))
        process.append(p)
        p.start()

    for p in process:
        p.join()

    cont = True
    while cont:
        if int(client.get("number_pushes")) >= number_petitions * 4:
            cont = False

    print(client.get("number_pushes"))

    elapsed = time.time() - start

    print(f"Time elapsed {elapsed}")

    return elapsed

if __name__ == "__main__":
    
    nodes = 3

    for i in range(nodes):
        client.delete(f"petitions_queue{i + 1}")

    results = {}

    for service in range(nodes):
        petition_queues(service + 1)
        initialize_insults()
        results[service] = []
        for petition in number_petitions:
            client.set("number_pushes", 0)
            print(f"Testing for {service + 1} node(s) and {petition} petitions...")
            time_elapsed = run_tests(petition, max_cpu)
            results[service].append(time_elapsed)

    for i in range(3):
        plt.plot(number_petitions, results[i], label=f"{i + 1} Nodes")
    
    plt.xlabel("Petitions")
    plt.ylabel("Time")
    plt.title("Test Stress Redis")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    speedup = [1, results[0][4] / results[1][4], results[0][4] / results[2][4]]
    workers = [1, 2, 3]

    plt.figure(figsize=(8, 5))
    markline, stemlines, baselline = plt.stem(
        workers, speedup, 
        linefmt='b-',
        markerfmt='bo-',
        basefmt='k-',
        label='Measeured Speedup'
    )

    plt.setp(stemlines, linewidth=2)

    plt.plot(workers, workers, 'r--', label='Ideal Speedup')

    plt.xlabel("Number of Workers")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Number of Workers", fontsize=14)

    plt.grid(True)
    plt.legend()
    plt.show()
