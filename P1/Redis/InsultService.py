import redis
import random
import time
import json
from multiprocessing import Process, Manager, Event


class InsultService:
    
    def __init__(self):
        self.client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
        self.instance_id = self.client.incr("insult_service_instance_id")
        self.insult_queue = "insult_queue"              
        self.channel_queue = "insult_channel"           
        self.petitions_queue = f"petitions_queue{self.instance_id}"        
        self.process = None

    # We define a function to add insults to our redis
    def add_insult(self, insult):      
        if insult not in self.get_insults():                   
            self.client.lpush(self.insult_queue, insult)        
            #print(f"Adding {insult}")  
        else:
            pass
            #print(f"The {insult} already exists")       

    # We define a function to remove an existing insult on our redis
    def remove_insult(self, insult):
        if insult in self.get_insults():
            self.client.lrem(self.insult_queue, 0, insult)
            print(f"Removing {insult}")
        else:
            print(f"The {insult} has already been removed")
    
    # We define a function to retrieve all the insults that are stored in our redis
    def retrieve_insults(self, client):
        print("Retrieving all insults on redis")
        self.client.lpush(client, *self.get_insults())

    # We define a function to send to the client a random insult
    def random_insult(self):
        return random.choice(self.get_insults())
    
    # We define a broadcast function where we send one random insult to each master subscriber
    def random_events(self, stop):
        insult_list = self.get_insults()
        while not stop.is_set():
            if insult_list:
                insult = self.random_insult()
                print(f"Publishing {insult}")
                self.client.publish(self.channel_queue, insult)
                time.sleep(5)
    
    # We define a function that returns all insults that are stored in our redis db 
    def get_insults(self):
        return self.client.lrange(self.insult_queue, 0, -1)
        
service = InsultService()
service.client.ltrim(service.petitions_queue, 1, 0)
print(service.petitions_queue)
print("Waiting for petitions...")
while True:
    _, raw_data = service.client.brpop(service.petitions_queue, timeout=0)
    petition = json.loads(raw_data)

    operation = petition["operation"]
    data = petition["data"]

    match operation:
        case "X1":
            service.add_insult(data)
        
        case "X2":
            service.retrieve_insults(data)

        case "X3":
            print("Activating broadcast")
            with Manager() as manager:
                stop = Event()
                list = manager.list(service.get_insults())
                service.process = Process(target=service.random_events, args=(stop,))
                service.process.start()
        
        case "X4":
            if service.process is not None:
                print("Stopping broadcast")
                stop.set()
                service.process.join()
            else:
                print("Broadcast is not active")

        case _:
            pass
    