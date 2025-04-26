from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random
import time
import multiprocessing
import xmlrpc.client
import redis

class MyFuncs:
    def __init__(self, insult_l):
        self.insult_list = insult_l
        self.subscribers_list = []
        self.process = None

    def add_subscriber(self, subscriber):
        if subscriber in self.subscribers_list:
            return f'{subscriber} EXIST'
        else:
            self.subscribers_list.append(subscriber)
            return f'{subscriber} ADDED' 

    def notify(self, insult_list, subscribers_list):
        while True:
            insult = random.choice(insult_list)
            print(f'Notify: {insult}')
            for subs in subscribers_list:
                s = xmlrpc.client.ServerProxy(subs)
                s.notifySub(insult)
            time.sleep(5)

    # Notify all the subscribers
    def notify_subscribers(self):
        if self.process is None:
            client_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            insult_list = client_redis.lrange(self.insult_list, 0, -1)
            self.process = multiprocessing.Process(target=self.notify, args=(insult_list, self.subscribers_list,))
            self.process.start()
            print(" [*] Notification Actived")
            return "Notification Actived"
        else:
            print(" [*] Notification is also Actived")
            return "Notification is also Actived"

    # Stop the notification
    def stop_subscribers(self):
        if self.process is not None:
            self.process.terminate()
            self.process.join()
            self.process = None
            print(" [*] Notification Desactived")
            return "Notification Desactived"
        else:
            print(" [*] Notification is also Desactived")
            return "Notification is also Desactived"

# Create server
if __name__ == "__main__":
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)
        
    with SimpleXMLRPCServer(('localhost', 8001),
                        requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_instance(MyFuncs('insult_list_n'))
        print("Broadcaster actived...")
        server.serve_forever()