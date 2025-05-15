import unittest
import redis
import random
import time
import json
from collections import Counter

# Before testing:
# - CleanIdentifier.py

# We need active:
# - InsultService.py (at least one instance)
# - InsultFilter.py (at least one instance)

class TestFilterRedis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        
        # We initialize a insult list to realize the test
        self.insults = ["idiota", "inútil", "tonto", "imbécil", "patán", "pesado", "torpe", "payaso", "estúpido", "malcriado"]

        # We initialize the redis client that we will be using on the functional tests bellow
        self.client = redis.Redis(host='localhost', port = 6379, db = 0, decode_responses = True)

        self.client.delete("insult_queue", "resolve_queue", "test_filter_queue", "petitions_queue", "filter_queue")

        time.sleep(1)

        for insult in self.insults:
            petition = {
                "operation" : "X1",
                "data" : insult
            }
            self.client.lpush("petitions_queue", json.dumps(petition))

        # We initialize the petition queue
        self.filter_queue = "filter_queue"

        # We initialize some petitions with the insults above
        self.petitions = [
            "No puedo creer que fueras tan idiota como para hacer eso.",
            "Hoy hace un clima espectacular para salir a caminar.",
            "Siempre llegas tarde, eres un inútil para organizarte.",
            "Tu presentación estuvo excelente, muy bien hecha.",
            "Deja de comportarte como un tonto, por favor.",
            "La película fue larga pero bastante entretenida.",
            "Ese imbécil casi choca mi coche esta mañana.",
            "Gracias por tu ayuda con el proyecto, fue muy valiosa."
        ]

        # We initialize the resolutions to the petitions above
        self.resolutions = [
            "No puedo creer que fueras tan CENSORED como para hacer eso.",
            "Hoy hace un clima espectacular para salir a caminar.",
            "Siempre llegas tarde, eres un CENSORED para organizarte.",
            "Tu presentación estuvo excelente, muy bien hecha.",
            "Deja de comportarte como un CENSORED, por favor.",
            "La película fue larga pero bastante entretenida.",
            "Ese CENSORED casi choca mi coche esta mañana.",
            "Gracias por tu ayuda con el proyecto, fue muy valiosa."
        ]

    def test_1_produce_work(self):
        for message in self.petitions:
            petition = {
                "operation" : "X1",
                "data" : message
            }
            self.client.lpush(self.filter_queue, json.dumps(petition))

    def test_2_consume_work(self):
        for _ in range(len(self.resolutions)):
            petition = {
               "operation" : "X2",
                "data" : ""
            }       
            self.client.lpush(self.filter_queue, json.dumps(petition))
    
    def test_3_retrive_resolutions(self):
        petition = {
            "operation" : "X3",
            "data" : "test_filter_queue"
        }
        self.client.lpush(self.filter_queue, json.dumps(petition))
        time.sleep(1)
        resolutions = self.client.lrange("test_filter_queue", 0, -1)
        assert Counter(resolutions) == Counter(self.resolutions)
        self.client.delete("test_filter_queue")
        

    @classmethod
    def tearDownClass(self):
        self.client.ltrim("insult_queue", 1, 0)
        self.client.ltrim("filter_queue", 1, 0)
        self.client.ltrim("resolve_queue", 1, 0)

if __name__ == '__main__':
    unittest.main()