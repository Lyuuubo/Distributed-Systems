import Pyro4
import redis
import random
import time
import statistics
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed


# We define the data that we will be using on the test phase
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
slaves_queue = "slaves_queue"
insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]
number_process = [100, 300, 600]
time_taken = []
max_workers = 50  

# Initialize slave services in Redis
for i in range(3):
    slave = f"insult" + str(i+1) + ".service"
    client.lpush(slaves_queue, slave)

# We define a function to make the stress test, this function is going to call add_insult from both structures
def add_insult_remotely(insult, nodes):
    ns = Pyro4.locateNS(host='localhost', port=9090)
    if nodes == 1:
        uri = ns.lookup('insult.service')
        server = Pyro4.Proxy(uri)
        server.add_insults(insult)
        server._pyroRelease()
    else:
        _, slave = client.brpop(slaves_queue, timeout=0)
        client.lpush(slaves_queue, slave)
        uri = ns.lookup(slave)
        proxy = Pyro4.Proxy(uri)
        proxy.add_insult(insult)
        proxy._pyroRelease()

# We define a function to run the test
def run_test(nodes):
    print(f"Stress test for {nodes} node(s)")
    results = []
    for count in number_process:
        print(f"  Number of processes: {count}")
        insults_sample = random.choices(insults, k=count)
        start = time.time()

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(add_insult_remotely, insult, nodes) for insult in insults_sample]
            for future in as_completed(futures):
                future.result()

        elapsed = time.time() - start
        results.append(elapsed)
        print(f"Elapsed: {elapsed:.3f}s")

    average = statistics.mean(results)
    time_taken.append(average)

# We deploy the test
run_test(1)
run_test(2)
run_test(3)

client.delete(slaves_queue)
print("Deleted Redis slave queue.")

# We procide to treat the data and generate the plot
speedup = [1, time_taken[0] / time_taken[1], time_taken[0] / time_taken[2]]
workers = [1, 2, 3]

print("Time taken:", time_taken)
print("Speedup:", speedup)

# Plot definition
plt.figure(figsize=(8, 5))
markerline, stemlines, baseline = plt.stem(
    workers, speedup,
    linefmt='b-',  # Line color (blue)
    markerfmt='bo',  # Marker style (blue circle)
    basefmt='k-',  # Baseline color (black)
    label='Measured Speedup'
)

# Customize spikes (optional: make them thicker)
plt.setp(stemlines, linewidth=2)

# Add ideal speedup line (linear scaling)
plt.plot(workers, workers, 'r--', label='Ideal Speedup')

# Labels and title
plt.xlabel('Number of Workers', fontsize=12)
plt.ylabel('Speedup', fontsize=12)
plt.title('Speedup vs Number of Workers', fontsize=14)

# Grid and ticks
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(workers)
plt.yticks([i * 1.0 for i in range(0, int(max(speedup)) + 2)])

# Legend
plt.legend()

# Show the plot
plt.show()
