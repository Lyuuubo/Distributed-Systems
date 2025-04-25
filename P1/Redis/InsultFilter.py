import redis
import json

class InsultFilter:
    
    def __init__(self):
        self.client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
        self.filter_queue = "filter_queue"
        self.petition_queue = "petition_queue"
        self.resolve_queue = "resolve_queue"
    
    def add_petition(self, petition):
        self.client.lpush(self.petition_queue, petition)

    def resolve_petition(self):
        _, petition = self.client.blpop(self.petition_queue, timeout=0)
        insults = self.client.lrange("insult_queue", 0, -1)
        print(insults)
        for insult in insults:
            if insult in petition:
                petition = petition.replace(insult, "CENSORED")
                break
        print(petition)
        self.client.lpush(self.resolve_queue, petition)
    
    def retrieve_resolutions(self, client):
        self.client.lpush(client, *self.get_resolve_queue())

    def get_resolve_queue(self):
        return self.client.lrange(self.resolve_queue, 0, -1)
    
filter = InsultFilter()

while True:
    print("Waiting for petitions to be filtered")
    _, raw_data = filter.client.blpop(filter.filter_queue, timeout=0)
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
