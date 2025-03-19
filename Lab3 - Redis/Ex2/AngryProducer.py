import redis
import time
import random

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "work_queue"

# Send multiple messages
tasks = ["Hola tonto", "Que tal perro", "Que passa feo", "Tinc gana gordo", "Mec mec cavero"]

while True:
    text = random.choice(tasks)
    client.rpush(queue_name, text)
    print(f"Produced: {text}")
    time.sleep(3) # Simulating a delay in task production