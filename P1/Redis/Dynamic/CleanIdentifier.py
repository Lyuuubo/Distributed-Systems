import redis

client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
client.set("insult_service_instance_id", 0)