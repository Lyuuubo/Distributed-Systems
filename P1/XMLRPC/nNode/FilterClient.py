import xmlrpc.client
import time
import random

master = xmlrpc.client.ServerProxy('http://localhost:8000')
url = master.connect_to_node()
print(f'Connect to: {url}')

s = xmlrpc.client.ServerProxy(url)

message_list = ['hola tonto','que tal','com estas','que feo ets deu meu',"cap d'espinaca",
                'dema a jugar a futbol gordo','fes el treball inutil','ves a passejar perro']

print('1 -> Producer')
print('2 -> Consumer')
print('3 -> See work_queue')
print('4 -> See result_queue')
option = input("Choice: ")

if option == '1':
    print('Producer:')
    while True:
        print(s.produce_work(random.choice(message_list)))
        time.sleep(5)
elif option == '2':
    print('Consumer:')
    while True:
        print(s.consume_work())
        time.sleep(3)
elif option == '3':
    print('work_queue:')
    while True:
        print(s.obtain_work_queue())
        time.sleep(8)
elif option == '4':
    print('result_queue:')
    while True:
        print(s.obtain_result_queue())
        time.sleep(4)
else:
    print('Bad choise: 1-4')
