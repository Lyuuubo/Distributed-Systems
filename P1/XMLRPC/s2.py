from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8002),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def notifySub(insult):
        print(f"Insult received: {insult}")
    server.register_function(notifySub, "notifySub")
     
    server.serve_forever()