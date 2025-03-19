import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name = "insult_subchanel"

# Subscribe to channel
pubsub = client.pubsub()
pubsub.subscribe(channel_name)
print(f"Subscribed to {channel_name}, waiting for messages...")

# Continuously listen for messages
for insult in pubsub.listen():
    if insult["type"] == "message":
        print(f"Received: {insult['data']}")