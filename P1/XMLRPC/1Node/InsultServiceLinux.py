from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random
import time
import multiprocessing
import argparse

class MyFuncs:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.insult_list = self.manager.list()
        self.subscribers_list = self.manager.list()
        self.ip_list = []
        self.process = None

    # Stores de insult in a list if not exist in
    def send_insult(self, insult):
        if insult in self.insult_list:
            return f'{insult} EXIST'
        else:
            self.insult_list.append(insult)
            return f'{insult} ADDED'
    
    def remove_insult(self, insult):
        if insult in self.insult_list:
            self.insult_list.remove(insult)
            return f'{insult} REMOVED'
        else:
            return f'{insult} NOT EXIST'

    # Return the list of insults
    def get_insults(self):
        return list(self.insult_list)

    # Return a random insult of the insult list
    def insult_me(self):
        return random.choice(self.insult_list)

    # Adds a sucriber. He received the url.
    def add_subscriber(self, subscriber):
        #s = xmlrpc.client.ServerProxy(subscriber)
        if subscriber in self.ip_list:
            return f'{subscriber} EXIST'
        else:
            self.ip_list.append(subscriber)
            self.subscribers_list.append(subscriber)
            return f'{subscriber} ADDED' 
    
    # Adds a subscriber. He received the url.
    def remove_subscriber(self, subscriber):
        #s = xmlrpc.client.ServerProxy(subscriber)
        if subscriber in self.subscribers_list:
            self.subscribers_list.remove(subscriber)
            return f'{subscriber} REMOVED'
        else:
            return f'{subscriber} NOT EXIST' 

    def notify(self, insult_list, subscribers_list):
        while True:
            insult = random.choice(insult_list)
            for subs in subscribers_list:
                s = xmlrpc.client.ServerProxy(subs)
                s.notifySub(insult)
            time.sleep(5)

    # Notify all the subscribers
    def notify_subscribers(self):
        if self.process is None:
            self.process = multiprocessing.Process(target=self.notify, args=(self.insult_list, self.subscribers_list,))
            self.process.start()
            return "Notification Actived"
        else:
            return "Notification is also Actived"

    # Stop the notification
    def stop_notify_subscribers(self):
        if self.process is not None:
            self.process.terminate()
            self.process.join()
            self.process = None
            return "Notification Desactived"
        else:
            return "Notification is also Desactived"
        
    # Restart server
    def reset(self):
        self.insult_list = self.manager.list()
        self.subscribers_list = self.manager.list()
        self.ip_list = []
        if self.process is not None:
            self.process.terminate()
            self.process.join()
            self.process = None
        return 'OK'

# Create server
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, help='Port where server listenning')

    args = parser.parse_args()  
    if args.port is None:
        port = 8200
    else:
        port = (int)(args.port)

    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)
        
    with SimpleXMLRPCServer(('localhost', port),
                        requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_instance(MyFuncs())
        print("Server actived...")
        server.serve_forever()

