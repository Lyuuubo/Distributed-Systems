import Pyro4    
import random
import time
import threading

@Pyro4.expose   
@Pyro4.behavior(instance_mode="single")
class InsultService:
    def __init__(self):
        self.insults = []
        self.subscribers = []
        self.thread = None
        self.stop = threading.Event()
           
    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            return f"Added insult: {insult}"
        return f"{insult} already exists"

    def remove_insult(self, insult):
        if insult in self.insults:
            self.insults.remove(insult)
            return f"Removed insult: {insult}"
        return f"{insult} not registered"
    
    def add_subscriber(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            return f"New subscriber {subscriber}"
        return f"Subscriber already added: {subscriber}"
    
    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            return f"Removed subscriber {subscriber}"
        return f"Subscriber already removed: {subscriber}"

    def notify(self, insult):
        self.add_insults(insult)

    def  get_insults(self):
        return self.insults
    
    def random_choice(self):
        return random.choice(self.insults)
    
    def get_subscribers(self):
        return self.subsribers
    
    def random_events(self):
        if self.thread is None or not self.thread.is_alive():
            self.stop.clear()
            self.thread = threading.Thread(target=self.auxiliar_random_events, daemon=True)
            self.thread.start()
            return 'random events activated'
        return 'already running'

    def auxiliar_random_events(self):
        while not self.stop.is_set():
            if self.subscribers and self.insults:
                for subscriber in self.subscribers:
                    sub = Pyro4.Proxy("PYRONAME:"+subscriber)
                    print(f"Insult sent {sub.notify(self.random_choice())}")
            time.sleep(5)

    def kill_random_events(self):
        if self.thread and self.thread.is_alive():
            self.stop.set()
            self.thread.join()
            self.thread = None
            return 'random events stopped'
        return 'no thread running'


daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = daemon.register(InsultService)
ns.register('insult.service', uri)
print(f"Server uri: {uri}")
daemon.requestLoop()