import redis
import json
import time

client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
filter_queue = "filter_queue"

petition = {
    "operation" : "X1",
    "data" : "Eres un marica, no sabes ni sumar."
}

client.lpush(filter_queue, json.dumps(petition))

petition = {
    "operation" : "X2",
    "data" : ""
}

client.lpush(filter_queue, json.dumps(petition))

petition = {
    "operation" : "X3",
    "data" : "client2_queue"
}

client.lpush(filter_queue, json.dumps(petition))

_, resolved = client.blpop("client2_queue", timeout=0)
print(resolved)