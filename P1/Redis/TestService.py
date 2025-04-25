import redis
import json
import time

client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
server_queue = "petitions_queue"

petition = {
    "operation" : "X1",
    "data" : "tonto"
}

client.lpush(server_queue, json.dumps(petition))

petition = {
    "operation" : "X1",
    "data" : "marica"
}

client.lpush(server_queue, json.dumps(petition))

petition = {
    "operation" : "X2",
    "data" : "client1_queue"
}

client.lpush(server_queue, json.dumps(petition))

petition = {
    "operation" : "X3",
    "data" : ""
}

client.lpush(server_queue, json.dumps(petition))

time.sleep(10)

petition = {
    "operation" : "X1",
    "data" : "retardado"
}

client.lpush(server_queue, json.dumps(petition))

time.sleep(10)

petition = {
    "operation" : "X4",
    "data" : ""
}

client.lpush(server_queue, json.dumps(petition))


