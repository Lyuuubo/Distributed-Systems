import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "insult_queue"
print("Consumer is waiting for insults...")

while True:
    insult = client.blpop(queue_name, timeout=0) 
    # Blocksindefinitely until a task is available
    if insult:
        print(f"Consumed: {insult[1]}")
        insults = client.lrange("insult_list", 0, -1)
        if insult[1] not in insults:
            client.lpush("insult_list", insult[1])
    