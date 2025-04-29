from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random
import redis

class MyFuncs:
    def __init__(self, insult_l):
        self.insult_list = insult_l
        self.broadcast = xmlrpc.client.ServerProxy('http://localhost:8001')
        self.client_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # Stores de insult in a list if not exist in
    def send_insult(self, insult):
        print(f" [*] Add insult: {insult}")
        insult_list = self.client_redis.lrange(self.insult_list, 0, -1)
        if insult in insult_list:
            return f'{insult} EXIST'
        else:
            self.client_redis.lpush(self.insult_list, insult)
            return f'{insult} ADDED'

    # Return the list of insults
    def get_insults(self):
        print(f" [>] Return insult list")
        return self.client_redis.lrange(self.insult_list, 0, -1)

    # Return a random insult of the insult list
    def insult_me(self):
        print(f" [>] Return random insult")
        insult_list = self.client_redis.lrange(self.insult_list, 0, -1)
        if len(insult_list) == 0: return "No Insult in list"
        return random.choice(insult_list)

    # Adds a sucriber. He received the url.
    def add_subscriber(self, subscriber):
        response =  self.broadcast.add_subscriber(subscriber)
        print(response)
        return response

    # Notify all the subscribers
    def notify_subscribers(self):
        response = self.broadcast.notify_subscribers()
        print(response)
        return response

    # Stop the notification
    def stop_notify_subscribers(self):
        response =  self.broadcast.stop_subscribers()
        print(response)
        return response
    
    def reset(self):
        print(' [!] Reset')
        self.broadcast.reset()
        self.client_redis.ltrim(self.insult_list, 1, 0)
        return "OK"

# Create server
if __name__ == "__main__":
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    s = xmlrpc.client.ServerProxy('http://localhost:8000')
    port = s.obtain_port()
    print(f'Assigned Port: {port}')
        
    with SimpleXMLRPCServer(('localhost', port),
                        requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_instance(MyFuncs('insult_list_n'))
        print("Slave actived...")
        server.serve_forever()

