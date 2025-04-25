import redis
import random
import time
import json
from multiprocessing import Process, Manager, Event

class InsultService:
    
    def __init__(self):
        self.client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)
        self.insult_queue = "insult_queue"              #Insult queue for the insult server (the redis clients won't have acces to it)
        self.channel_queue = "insult_channel"           #This is the channel where all the redis clients will access to recieve the broadcast
        self.petitions_queue = "petitions_queue"        #This is the queue where all the petitions from the clients will be stored
        self.process = None

    def add_insult(self, insult):
        insult_list = self.get_insults()                
        if insult not in insult_list:                   
            print(f"Adding {insult}")
            self.client.lpush(self.insult_queue, insult)                     

    def remove_insult(self, insult):
        insult_list = self.get_insults()
        if insult in insult_list:
            print(f"Removing {insult}")
            self.client.lrem(self.insult_queue, 0, insult)
    
    def retrieve_insults(self, client):
        self.client.lpush(client, *self.get_insults())

    def random_insult(self):
        insult_list = self.get_insults()
        return random.choice(insult_list)
    
    def random_events(self, stop):
        insult_list = self.get_insults()
        while not stop.is_set():
            if insult_list:
                insult = self.random_insult()
                print(f"Publishing {insult}")
                self.client.publish(self.channel_queue, insult)
                time.sleep(5)

    def get_insults(self):
            return self.client.lrange(self.insult_queue, 0, -1)
    
service = InsultService()

while True:
    print("Waiting for petitions...")
    _, raw_data = service.client.blpop(service.petitions_queue, timeout=0)
    print("Petition recived")
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
            print("Non existing operation")
    