import Pyro4
import time
import multiprocessing
from matplotlib import pyplot as plt


# We need active:
# - ActiceServer.py
# - Static/InsultService.py 

service_name = "insult.service"
insult_list = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_petitions = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
max_cpu = 4
ns = Pyro4.locateNS()

# We add all the insults in the service (it doesn't bother if its nNodes implementation cause we have a redis list with the insults)
def initialize_insults():
    for insult in insult_list:
        uri = ns.lookup(service_name)
        server = Pyro4.Proxy(uri)
        server.add_insult(insult)

# We retrieve insults for all the number of petitions that the client indicates
def insult_getter(number_petitions, counter, block, reference):
    for _ in range(number_petitions):
        Pyro4.Proxy(reference).random_choice()
        with block:
            counter.value += 1
    
# We define a function to do the testing
def run_tests(number_petitions, number_process):
    counter = multiprocessing.Value('i', 0)
    block = multiprocessing.Lock()
    process = []
    references = ns.lookup(service_name)

    start = time.time()

    for _ in range(number_process):  
        p = multiprocessing.Process(target=insult_getter, args=(number_petitions, counter, block, references))
        process.append(p)
    
    for p in process:
        p.start()

    for p in process:
        p.join()

    elapsed = time.time() - start

    print(f"Time elapsed {elapsed}")

    return elapsed

if __name__ == "__main__":

    results = {}

    print(service_name)

    # We initialize the insult list for all the insult servers defined
    initialize_insults()
    
    # We define a list for each service
    results = []

    for petition in number_petitions:
        print(f"Testing fo node(s) and {petition} petitions...")
        time_elapsed = run_tests(petition, max_cpu)
        results.append(time_elapsed)

    print(results)

    plt.plot(number_petitions, results, 'b-', label='Real')
    
    plt.xlabel("Petitions")
    plt.ylabel("Time")
    plt.title("Test Stress Pyro")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()