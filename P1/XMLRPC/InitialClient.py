import xmlrpc.client
import time

s = xmlrpc.client.ServerProxy('http://localhost:8000')

# Print list of available methods
#print(s.system.listMethods())
print(s.send_insults("MEC"))
print(s.send_insults("cap d'espinaca"))
print(s.send_insults("Kevin"))
#print(s.get_insults())
#print(s.insult_me())
print(s.add_subscriber('http://localhost:8001'))
print(s.add_subscriber('http://localhost:8002'))
#print(s.notify_subscribers())
#time.sleep(10)
#print(s.stop_notify_subscribers())
