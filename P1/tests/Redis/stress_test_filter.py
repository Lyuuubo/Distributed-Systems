import redis
import time
import statistics
import random
import json
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# We define the data that we will be using on the test phase
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

petitions = [
    "No puedo creer que fueras tan idiota como para hacer eso.",
    "Hoy hace un clima espectacular para salir a caminar.",
    "Siempre llegas tarde, eres un inútil para organizarte.",
    "Tu presentación estuvo excelente, muy bien hecha.",
    "Deja de comportarte como un tonto, por favor.",
    "La película fue larga pero bastante entretenida.",
    "Ese imbécil casi choca mi coche esta mañana.",
    "Gracias por tu ayuda con el proyecto, fue muy valiosa."
]

number_process = [50, 100, 200, 300, 400]
time_taken = []
max_workers = 50  
client.ltrim("filter_queue", 1, 0)

# We define a function to make the stress test, this function is going to call add_insult from both structures
def add_message_remotely():
    message = random.choice(petitions)
    petition = {
        "operation": "X1",
        "data": message
    }
    client.lpush("filter_queue", json.dumps(petition))

# We define a function to run the test
def run_test(nodes):
    print(f"Stress test for {nodes} node(s)")
    results = []
    
    for count in number_process:
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(add_message_remotely) for _ in range(count)]
            for future in futures:
                future.result()  # Asegura que todas las tareas se han completado
        
        elapsed = time.time() - start
        results.append(elapsed)
        print(f"Elapsed: {elapsed:.3f}s")
    
    average = statistics.mean(results)
    time_taken.append(average)

# We deploy the test
run_test(1)
run_test(2)
run_test(3)

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
