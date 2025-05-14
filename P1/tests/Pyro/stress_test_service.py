import Pyro4
import time
import multiprocessing
import statistics
from itertools import cycle
from matplotlib import pyplot as plt


# We need active:
# - ActiceServer.py
# - Static/InsultService.py 

service_names = []
insult_list = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_petitions = [1]
max_cpu = 8
ns = Pyro4.locateNS()

# We add all the insults in the service (it doesn't bother if its nNodes implementation cause we have a redis list with the insults)
def initialize_insults():
    for insult in insult_list:
        uri = ns.lookup(service_names[0])
        server = Pyro4.Proxy(uri)
        server.add_insult(insult)

# We initialize all the nodes for test 
def initialize_nodes():
    service_names.clear()
    service_names.append("insult.service")

# We retrieve insults for all the number of petitions that the client indicates
def insult_getter(number_petitions, counter, block, reference):
    while counter.value < number_petitions:
        Pyro4.Proxy(reference).random_choice()
        with block:
            counter.value += 1
    
# We define a function to do the testing
def run_tests(number_petitions, number_process):
    counter = multiprocessing.Value('i', 0)
    block = multiprocessing.Lock()
    process = []
    references = [ns.lookup(namespace) for namespace in service_names]

    start = time.time()

    for _ in range(number_process):  
        p = multiprocessing.Process(target=insult_getter, args=(number_petitions, counter, block, references))
        process.append(p)
        p.start()

    for p in process:
        p.join()

    elapsed = time.time() - start

    print(f"Time elapsed {elapsed}")

    return elapsed

if __name__ == "__main__":

    results = {}

    # We run the tests
    initialize_nodes()

    print(service_names)

    # We initialize the insult list for all the insult servers defined
    initialize_insults()
    
    # We define a list for each service
    results = []

    for petition in number_petitions:
        print(f"Testing fo node(s) and {petition} petitions...")
        time_elapsed = run_tests(petition, max_cpu)
        results.append(time_elapsed)

    for i in range(3):
        plt.plot(number_petitions, results[i], label=f"{i + 1} Nodes")
    
    plt.xlabel("Petitions")
    plt.ylabel("Time")
    plt.title("Test Stress Pyro")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()