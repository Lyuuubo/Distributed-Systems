from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import redis
import xmlrpc.client

class MyFuncs:
    def __init__(self, work, result):
        self.insult_list = ['tonto', 'inutil', "cap d'espicana", 'cavero', 'gordo', 'feo', 'perro']
        self.work_queue = work
        self.result_queue = result
        self.client_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def produce_work(self, message):
        self.client_redis.lpush(self.work_queue, message)
        print(f"Produce work: {message}")
        return f"Produce work: {message}"
    
    def consume_work(self):
        work = self.client_redis.lpop(self.work_queue)
        text = work
        if work is not None:
            print(f'Consume work: {work}')
            for insult in self.insult_list:
                if insult in work:
                    text = work.replace(insult, "CENSORED")
                    break
            print(text)
            self.client_redis.lpush(self.result_queue, text)  
            return f'Consume work: {work} -> {text}'
        else: return 'Any work in the queue'

    def obtain_result_queue(self):
        result = self.client_redis.lrange(self.result_queue, 0, -1)
        return result

    def obtain_work_queue(self):
        work = self.client_redis.lrange(self.work_queue, 0, -1)
        return work

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
        server.register_instance(MyFuncs('work_queue', 'result_queue'))
        print("Filter actived...")
        server.serve_forever()