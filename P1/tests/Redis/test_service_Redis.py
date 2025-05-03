import unittest
import redis
import random
import time
import json
from collections import Counter

# We need active:
# - InsultService.py (at least one instance)
class TestServiceRedis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        
        # We initialize a insult list to realize the test
        self.insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]

        # We initialize the redis client that we will be using on the functional tests bellow
        self.client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)

        # We initialize the petition queue
        self.petition_queue = "petitions_queue"

    def test_1_add_insult(self):
        for insult in self.insults:
            petition = {
                "operation" : "X1",
                "data" : insult
            }
            self.client.lpush(self.petition_queue, json.dumps(petition))

        petition = {
            "operation" : "X1",
            "data" : random.choice(self.insults)
        }
        self.client.lpush(self.petition_queue, json.dumps(petition))

    # It goes wrong some times 
    def test_2_retrieve_insults(self):
        petition = {
            "operation" : "X2",
            "data" : "test_service_queue"
        }

        self.client.lpush(self.petition_queue, json.dumps(petition))
        time.sleep(1)
        response = self.client.lrange("test_service_queue", 0, -1)
        assert Counter(response) == Counter(self.insults)
        self.client.delete("test_service_queue")
    
    def test_3_start_broadcast(self):
        petition = {
            "operation" : "X3",
            "data" : ""
        }

        self.client.lpush(self.petition_queue, json.dumps(petition))
        time.sleep(10)

    def test_4_stop_broadcast(self):
        petition = {
            "operation" : "X4",
            "data" : ""
        }

        self.client.lpush(self.petition_queue, json.dumps(petition))

    @classmethod
    def tearDownClass(self):
        self.client.ltrim("insult_queue", 1, 0)
        self.client.ltrim("resolve_queue", 1, 0)

if __name__ == '__main__':
    unittest.main()