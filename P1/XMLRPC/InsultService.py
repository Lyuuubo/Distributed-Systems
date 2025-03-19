from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random
import time
import threading

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    insult_list = []
    subscribers_list = []
    ip_list = []
    thread = None

    def send_insults(insult):
        if insult in insult_list:
            return f'{insult} EXIST'
        else:
            insult_list.append(insult)
            return f'{insult} ADDED'
    server.register_function(send_insults, "send_insults")

    def get_insults():
        return insult_list
    server.register_function(get_insults, "get_insults")

    def insult_me():
        return random.choice(insult_list)
    server.register_function(insult_me, "insult_me")

    def add_subscriber(subscriber):
        s = xmlrpc.client.ServerProxy(subscriber)
        if subscriber in ip_list:
            return f'{subscriber} EXIST'
        else:
            ip_list.append(subscriber)
            subscribers_list.append(s)
            return f'{subscriber} ADDED' 
    server.register_function(add_subscriber, "add_subscriber")
        
    def notify():
        for subs in subscribers_list:
            subs.notifySub(random.choice(insult_list))
        time.sleep(5)

    def notify_subscribers():
        notify()
        #if thread is None:
         #   thread = threading.Thread(target=notify)
          #  thread.start()
           # return "Notification actived"
        #else:
         #   return "Notification is also actived"
    server.register_function(notify_subscribers, "notify_subscribers")

    def stop_notify_subscribers():
        if thread is not None:
            thread.join()
            return "Succes in stop notification"
        else:
            return "Any notification is active"
    server.register_function(stop_notify_subscribers, "stop_notify_subscribers")
     
    server.serve_forever()

