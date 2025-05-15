import redis
import time
import multiprocessing
import json
import random
from itertools import cycle
from matplotlib import pyplot as plt

# We need active:
# - Static/InsultService.py

client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
service_queues = "petitions_queue"
insult_list = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_petitions = [1000, 2000, 5000, 10000, 50000, 100000, 500000]
max_cpu = 4

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
    petition = {
        "operation" : "X5",
        "data" : ""
    }
    for _ in range(number_petitions):
        client.lpush(service_queues, json.dumps(petition))
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

    results = []

    for petition in number_petitions:
        client.set("number_pushes", 0)
        print(f"Testing for 1 node and {petition} petitions...")
        time_elapsed = run_tests(petition, max_cpu)
        results.append(time_elapsed)

    plt.plot(number_petitions, results, 'b-', label='Real')
    
    plt.xlabel("Petitions")
    plt.ylabel("Time")
    plt.title("Test Stress Redis")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()