import Pyro4
import time
import multiprocessing
from matplotlib import pyplot as plt

service_names = []
insult_list = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_petitions = [1000, 2000, 3000, 4000, 5000]
max_cpu = 4

# We retrieve insults for all the number of petitions that the client indicates
def insult_getter(number_petitions, counter, block):
    pass

# We define a function to do the testing
def run_tests(number_petitions, number_process):
    counter = multiprocessing.Value('i', 0)
    block = multiprocessing.Lock()
    process = []

    start = time.time()

    for _ in range(number_process):  
        p = multiprocessing.Process(target=insult_getter, args=(number_petitions, counter, block))
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
        
        # We define a list for each service
        results[service] = []

        for petition in number_petitions:
            print(f"Testing for {service + 1} node(s) and {petition} petitions...")
            time_elapsed = run_tests(petition, max_cpu)
            results[service].append(time_elapsed)




