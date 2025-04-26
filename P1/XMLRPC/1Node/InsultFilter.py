from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from collections import deque

class MyFuncs:
    def __init__(self):
        self.insult_list = ['tonto', 'inutil', "cap d'espicana", 'cavero', 'gordo', 'feo', 'perro']
        self.work_queue = deque()
        self.result_queue = deque()

    def produce_work(self, message):
        self.work_queue.append(message)
        print(f"Produce work: {message}")
        return f"Produce work: {message}"
    
    def consume_work(self):
        try:
            work = self.work_queue.popleft()
            text = work
            print(f'Consume work: {work}')
            for insult in self.insult_list:
                if insult in work:
                    text = work.replace(insult, "CENSORED")
                    break
            print(text)
            self.result_queue.append(text)
            return f'Consume work: {work} -> {text}'
        except IndexError:
            return 'Any work in the queue'

    def obtain_result_queue(self):
        return list(self.result_queue)

    def obtain_work_queue(self):
        return list(self.work_queue)

# Create server
if __name__ == "__main__":
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)
        
    with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_instance(MyFuncs())
        print("Server actived...")
        server.serve_forever()