import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "work_queue"
result_list = "result_list"
print("Consumer is waiting for tasks...")
insults = ["tonto","perro","feo","gordo","cavero"]

while True:
    task = client.blpop(queue_name, timeout=0) 
    # Blocksindefinitely until a task is available
    if task:
        text = task[1]
        for insult in insults:
            if insult in text:
                text = text.replace(insult, "CENSORED")
                break
        print(text)
        client.lpush(result_list, text)