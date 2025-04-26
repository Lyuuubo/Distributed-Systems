import xmlrpc.client
import time

s = xmlrpc.client.ServerProxy('http://localhost:8000')

print(s.notify_subscribers())
time.sleep(100)
print(s.stop_notify_subscribers())
