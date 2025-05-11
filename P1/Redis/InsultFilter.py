import redis
import json

class InsultFilter:
    
    def __init__(self):
        self.client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
        self.instance_id = self.client.incr("insult_service_instance_id")
        self.filter_queue = f"filter_queue{self.instance_id}"
        self.petition_queue = "petition_queue"
        self.resolve_queue = "resolve_queue"
    
    # We define a function to store filter petitions from clients
    def add_petition(self, petition):
        self.client.lpush(self.petition_queue, petition)
        print(f"Adding new petition: {petition}")

    # We define a function to resolve one a petition
    def resolve_petition(self):
        _, petition = self.client.brpop(self.petition_queue, timeout=0)
        insults = self.client.lrange("insult_queue", 0, -1)
        for insult in insults:
            if insult in petition:
                petition = petition.replace(insult, "CENSORED")
        self.client.lpush(self.resolve_queue, petition)
        print(f"Resolved petition: {petition}")
    
    # We define a function to retrieve all the resolutions
    def retrieve_resolutions(self, client):
        print("Retriving all resolutions")
        self.client.lpush(client, *self.get_resolve_queue())

    # We define a functino to get all the resolutions (this function is meant to be private)
    def get_resolve_queue(self):
        return self.client.lrange(self.resolve_queue, 0, -1)
    
filter = InsultFilter()
print("Waiting for petitions to be filtered")
while True:
    _, raw_data = filter.client.brpop(filter.filter_queue, timeout=0)
    print("Petition recieved")
    petition = json.loads(raw_data)

    operation = petition["operation"]
    data = petition["data"]

    match operation:
        case "X1":
            filter.add_petition(data)
        
        case "X2":
            filter.resolve_petition()

        case "X3":
            filter.retrieve_resolutions(data)

        case _:
            print("Non exisiting operation")
