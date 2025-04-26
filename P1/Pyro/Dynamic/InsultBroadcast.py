import Pyro4
import redis
import random

class InsultBroadcast:
    
    def __init__(self):
        self.client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True)
        self.insult_list = "insult_list"
        self.subscriber_list = "subscriber_list"

    def start_broadcast(self):
        subscriber_list = self.client.lrange(self.subscriber_list, 0, -1)
        insult_list = self.client.lrange(self.insult_list, 0, -1)
        for uri in subscriber_list:
            subscriber = Pyro4.Proxy(uri)
            subscriber.notify_subscriber(random.choice(insult_list))



