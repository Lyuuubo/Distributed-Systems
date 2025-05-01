import Pyro4   
import redis 
import random
import base64
from multiprocessing import Process, Manager
from InsultBroadcast import InsultBroadcast
from InsultFather import InsultFather


@Pyro4.expose   
class InsultService(InsultFather):

    def __init__(self):
        self.client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True)
        self.insult_list = "insult_list"
        self.subscriber_list = "subscriber_list"
        self.p = None
        super().__init__(False)
           
    # We define a function to store an insult that is not in the redis database
    def add_insult(self, insult):
        if insult not in self.get_insults():
            print(f"Adding new insult {insult}")
            self.client.lpush(self.insult_list, insult)
            return f"Adding new insult {insult}"
        print(f"The {insult} is already stored")
        return f"The {insult} is already stored"
    
    # We define a function that removes an insult that is in the redis database
    def remove_insult(self, insult):
        if insult in self.get_insults():
            print(f"Removing insult {insult}")
            self.insult_list.lrem(self.insult_list, 0, insult)
    
    # We define a function to register new subscribers to the database
    def add_subscriber(self, uri):

        # We use base64 encode import to add new subcribers because redis doesn't acces uri 
        byte_uri = str(uri).encode('utf-8')
        encoded_uri = base64.urlsafe_b64encode(byte_uri)
        if encoded_uri.decode('utf-8') not in self.get_subscribers():
            self.client.lpush(self.subscriber_list, encoded_uri)
            print(f"Adding new subscriber {uri}")
            return f"Adding new subscriber {uri}"
        print (f"The subscriber {uri} is already stored")
        return f"The subscriber {uri} is already stored"

    # We define a function to remove a subscriber from redis
    def remove_subscriber(self, uri):
        byte_uri = str(uri).encode('utf-8')
        encoded_uri = base64.urlsafe_b64encode(byte_uri)
        if encoded_uri.decode('utf-8') in self.get_subscribers():
            self.client.lrem(self.subscriber_list, 0, encoded_uri)
            print(f"Removing subscriber {uri}")
            return f"Removing subscriber {uri}"
        print(f"The subscriber {uri} is already removed")
        return f"The subscriber {uri} is already removed"

    # We define a function to clean all insults
    def clean_insults(self):
        print("Cleaning all insults on redis")
        self.client.ltrim(self.insult_list, 1, 0)

    # We define a function to clean all subscribers
    def clean_subscribers(self):
        print("Cleaning all subscribers on redis")
        self.client.ltrim(self.subscriber_list, 1, 0)

    # We define a function that returns a random insult from the storage
    def random_choice(self):
        return random.choice(self.get_insults())

    # We define a function that allows the clients to retrieve the whole insult list
    def get_insults(self):
        return self.client.lrange(self.insult_list, 0, -1)
    
    # We define a functino that allows us to retrieve all the subscribers from the master server
    def get_subscribers(self):
        return self.client.lrange(self.subscriber_list, 0, -1)

    # We define a broadcast function starter that creates a process of broadcast_function that notifies periodically the subscribers from the master
    def start_broadcast(self):
        if self.p is None:
            with Manager() as manager:
                broadcaster = InsultBroadcast()
                self.p = Process(target=broadcaster.broadcast_function)
                self.p.start()
            return 'Starting broadcast'
        else:
            return 'Broadcast is already started'

    # We define the broadcast killing function
    def kill_broadcast(self):
        if self.p is not None:
            self.p.terminate()
            self.p.join()
            self.p.close()
            self.p = None
            return 'Finishing broadcast'
        else:
            return 'Broadcast function its already dead'