import redis
import time
import random

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name = "insult_subchanel"

# Publish multiple messages
insults = ["Tonto", "Perro", "Cap d'espinaca", "Gordo", "Feo","Cavero"]

while True:
    insult = random.choice(insults)
    client.publish(channel_name, insult)
    print(f"Published: {insult}")
    time.sleep(5) # Simulating delay between messages