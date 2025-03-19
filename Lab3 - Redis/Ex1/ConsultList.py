import redis

# Connect to Redis server
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Get all elements from the list
fruits = client.lrange("insult_list", 0, -1)
print(f"Insult list: {fruits}")