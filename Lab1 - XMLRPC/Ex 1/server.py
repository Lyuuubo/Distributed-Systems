from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import random

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    llista_insults = []
    def add_insults(insult):
        if insult in llista_insults:
            return f'{insult} EXIST'
        else:
            llista_insults.append(insult)
            return f'{insult} ADDED'
    server.register_function(add_insults, "add_insults")

    def get_insults():
        return llista_insults
    server.register_function(get_insults, "get_insults")

    def insult_me():
        return random.choice(llista_insults)
    server.register_function(insult_me, "insult_me")

    server.serve_forever()

