import xmlrpc.client
import time
import random

master = xmlrpc.client.ServerProxy('http://localhost:8000')
url = master.connect_to_node()
print(f'Connect to: {url}')

s = xmlrpc.client.ServerProxy(url)

insults = ["Perro", "Cabron", "Tonto", "Marica"]

while True:
    print('1 -> Send Insults')
    print('2 -> Insult Me + Get Insults')
    print('3 -> Add Suscribers')
    print('4 -> Start Broadcast')
    print('5 -> Stop Broadcast')
    option = input("Choice: ")

    if option == '1':
        print('Send insults:')
        for insult in insults:
            print(s.send_insult(insult))
            time.sleep(1)
    elif option == '2':
        print('Insult Me + Get Insults:')
        print(s.insult_me())
        print(s.insult_me())
        print(s.insult_me())
        print(s.get_insults())
    elif option == '3':
        print('Add Suscriber:')
        print(s.add_subscriber('http://localhost:8101'))
        print(s.add_subscriber('http://localhost:8102'))
        print(s.add_subscriber('http://localhost:8103'))
    elif option == '4':
        print('Start Broadcast')
        print(s.notify_subscribers())
    elif option == '5':
        print('Stop Broadcast')
        print(s.stop_notify_subscribers())
    else:
        print('Bad choise: 1-5')
    print('<------------>')
    time.sleep(2)