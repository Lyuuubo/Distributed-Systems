import Pyro4   
import redis 
import random

@Pyro4.expose   
class InsultService:
    def __init__(self):
        self.client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True)
        self.insult_list = "insult_list"
        self.subscriber_list = "subscriber_list"
           
    def add_insult(self, insult):
        if insult not in self.get_insults():
            print(f"Adding new insult {insult}")
            self.client.lpush(self.insult_list, insult)
    
    def remove_insult(self, insult):
        if insult in self.get_insults():
            print(f"Removing insult {insult}")
            self.insult_list.lrem(self.insult_list, 0, insult)
    
    
    def add_subscriber(self, uri):
        if uri not in self.get_subscribers():
            print(f"Adding new subscriber {uri}")
            self.client.lpush(self.subscriber_list, uri)

    def remove_subscriber(self, uri):
        if uri in self.get_subscribers():
            print(f"Removing subscriber {uri}")
            self.client.lrem(self.subscriber_list, 0, uri)

    def notify_sub(self, message):
        print(f"Message recieved: {message}")

    def clean_insults(self):
        self.client.ltrim(self.insult_list, 1, 0)

    def clean_subscribers(self):
        self.client.ltrim(self.subscriber_list, 1, 0)

    def random_choice(self):
        return random.choice(self.get_insults())

    def get_insults(self):
        return self.client.lrange(self.insult_list, 0, -1)
    
    def get_subscribers(self):
        return self.client.lrange(self.subscriber_list, 0, -1)
