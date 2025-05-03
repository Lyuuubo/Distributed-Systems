from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random
import time
from collections import deque

class MyFuncs:
    def __init__(self):
        self.nodes = deque()      # Queue with active nodes
        self.next_port = 8002           # Assignation of port to specific node

    # Return de port to specific node
    def obtain_port(self):
        port = self.next_port
        url = f'http://localhost:{port}'
        self.next_port = self.next_port + 1
        self.nodes.appendleft(url)
        print(f" [*] New Node: {url}")
        return port

    # Return the url of a node
    def connect_to_node(self):
        if len(self.nodes) > 0:
            url = self.nodes.popleft()
            self.nodes.append(url)
            print(f" [>] Return Node: {url}")
            return url
        else: return "Any Node is active"
    
    def get_urls(self):
        print(f" [>] Return URL's queue")
        return list(self.nodes)
    
    def reset(self):
        print(' [!] Reset')
        s = xmlrpc.client.ServerProxy(self.nodes[0])
        s.reset()
        return "OK"

# Create server
if __name__ == "__main__":
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)
        
    with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_instance(MyFuncs())
        print("Master actived...")
        server.serve_forever()