import Pyro4
import time
import multiprocessing
import statistics
from itertools import cycle
from matplotlib import pyplot as plt


# We need active:
# - ActiceServer.py
# - Static/InsultService.py 
# - Dynamic/InsultMaster.py
# - Dynamic/InsultSlaveService.py (3 instances)

service_names = []
insult_list = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_petitions = [1000, 2000, 3000, 4000, 5000]
max_cpu = 4
ns = Pyro4.locateNS()

# We initialize all the nodes for test (1, 2, 3)
def initialize_nodes(nodes):
    service_names.clear()
    if nodes > 1:
        for i in range(nodes):
            service_names.append("insult" + str(i + 1) + ".service")
    else:
        service_names.append("insult.service")
    print(service_names)

# We add all the insults in the service (it doesn't bother if its nNodes implementation cause we have a redis list with the insults)
def initialize_insults():
    for insult in insult_list:
        uri = ns.lookup(service_names[0])
        server = Pyro4.Proxy(uri)
        server.add_insult(insult)

# We retrieve insults for all the number of petitions that the client indicates
def insult_getter(number_petitions, counter, block, references):
    service_rr = cycle(references)
    while counter.value < number_petitions:
        Pyro4.Proxy(next(service_rr)).random_choice()
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
    
    nodes = 3

    results = {}

    # We run the tests

    for service in range(nodes):

        # We initialize the namespaces for the insult servers
        initialize_nodes(service + 1)

         # We initialize the insult list for all the insult servers defined
        initialize_insults()
        
        # We define a list for each service
        results[service] = []

        for petition in number_petitions:
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
    print(speedup)
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