import Pyro4
import redis
import random
import time
import base64

class InsultBroadcast:
    
    def __init__(self):
        self.client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True)
        self.insult_list = "insult_list"
        self.subscriber_list = "subscriber_list"

    # We define a broadcast function where we send one random insult to each master subscriber
    def broadcast_function(self):
        while True:

            # We retrieve subscriber list and insult list
            subscriber_list = self.client.lrange(self.subscriber_list, 0, -1)
            insult_list = self.client.lrange(self.insult_list, 0, -1)
            for uri in subscriber_list:
                subscriber = base64.urlsafe_b64decode(uri).decode('utf-8')
                subscriber = Pyro4.Proxy(subscriber)
                subscriber.notify_sub(random.choice(insult_list))
            time.sleep(5)



