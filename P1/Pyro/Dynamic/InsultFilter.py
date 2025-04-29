import Pyro4
import redis
from InsultFather import InsultFather

@Pyro4.expose 
class InsultFilter(InsultFather):

    def __init__(self):
        self.client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True)
        self.insult_list = "insult_list"
        self.petition_list = "petition_list"
        self.resolve_list = "resolve_list"
        super().__init__(True)

    # We define a fuction to sotre new filter petitions
    def add_petition(self, message):
        print(f"Adding new petition {message}")
        self.client.lpush(self.petition_list, message)

    # We define a function to resolve the oldest petition stored
    def resolve_petition(self):
        petition = self.client.lpop(self.petition_list)
        if petition is not None:
            insults = self.client.lrange(self.insult_list, 0 , -1)
            for insult in insults:
                if insult in petition:
                    petition = petition.replace(insult, "CENSORED")
                    break
            self.client.lpush(self.resolve_list, petition)
        else:
            print("No job to be done")

    # We define a function to retrieve all the resolutions stored
    def retrieve_resolutions(self):
        return self.client.lrange(self.resolve_list, 0, -1)
    
    # We define a function to clean the redis list that store the resolutions
    def clean_resolutions(self):
        self.client.ltrim(self.resolve_list, 1, 0)

