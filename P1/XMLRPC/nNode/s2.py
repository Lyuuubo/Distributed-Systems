from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

if __name__ == "__main__":
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    # Create server
    with SimpleXMLRPCServer(('localhost', 8102),
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def notifySub(insult):
            print(f"Insult received: {insult}")
            return "ok"
        server.register_function(notifySub, "notifySub")
        
        print("S2 actived...")
        server.serve_forever()
