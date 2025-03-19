from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8002),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    llista_insults = []
    llista_observers = []
    llista_ip = []
    def add_insults(insult):
        if insult in llista_insults:
            return f'{insult} EXIST'
        else:
            llista_insults.append(insult)
            for x in llista_observers:
                print(x.notify())
            return f'{insult} ADDED'
    server.register_function(add_insults, "add_insults")

    def get_insults():
        return llista_insults
    server.register_function(get_insults, "get_insults")

    def insult_me():
        return random.choice(llista_insults)
    server.register_function(insult_me, "insult_me")

    def add_observer(ip_port):
        s = xmlrpc.client.ServerProxy(ip_port)
        if ip_port in llista_ip:
            return f'{ip_port} EXIST'
        else:
            llista_ip.append(ip_port)
            llista_observers.append(s)
            return f'{ip_port} ADDED' 
    server.register_function(add_observer, "add_observer")

    def notify(insult):
        print(f'{insult} ADDED OBSERVER')
        return ""
    server.register_function(notify, "notify")


    server.serve_forever()

