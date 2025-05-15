# Distributed-Systems

## Pràctica 1:

Aquest repositori conté 2 aplicacions escalables implementades amb quatre middlewares de comunicació diferents: XMLRPC, Pyro, Redis i RabbitMQ.

Aquestes dues aplicacions són, d’una primera instància, el InsultService, el qual ha de rebre insults remotament i poder-los emmagatzemar. També ha de proporcionar un mecanisme per poder realitzar missatges broadcast cada 5 segons, notificant events aleatoris als subscriptors interessats. 

Per altra banda, tenim el InsultFIlter, el qual és un servei basat en el patró Work queue. Aquest servei implementarà un mecanisme de filtratge d’insults, on substituirà els insults del text per la paraula CENSORED.

També conté un sistema d’escalat dinàmic, el qual va escalant nodes segons el número d'events que arriben. Aquesta implementació s'ha realitzat amb RabbitMQ.

## Serveis actius

Per executar el codi amb els diferents middlewares necessitem els següents serveis: redis-server i rabbitmq-server.
```python
# Install redis and rabbitmq
sudo apt install redis-server -y
sudo apt install rabbitmq-server -y
```

## Dependències

```python
# Install Python client for Redis and Rabbit
pip3 install redis
pip3 intall pika

# Install Pyro4
pip3 install Pyro4
```

## Com executar els tests?

En la carpeta de tests, disposem de tots els fitxers que s'han usat per provar el correcte funcionament dels serveis i els que s'han usat per fer l'stress test i la comparació de speedup. Al principi de tot, tenim comentats quins són els processos que han d'estar corrent abans d'executar el test (recomanable en una altra terminal):

![image](https://github.com/user-attachments/assets/ecb955ac-b856-4235-95ec-c036ade9897a)

En aquest exemple, podem observar com per poder executar el test del InsultService de XMLRPC, necessitem tenir el Master, vàies instàncies de l'Slave, el Broadcast i 1 o vàries instàncies dels subscriptors.

## Comprovar el dynamic scaling

Per realitzar una comprovació del dinàmic scaling, tenim dues opcions:

  1 - Executar en una terminal el dynamic/Main.py, en un o diversos terminals diferents el dynamic/Client.py i observar visualment a partir de la terminal com escala (segons el nombre de clients).
  
  2 - Executar el dynamic/TestMaster.py el qual és un test que va enviant diferentes ràfagues devents a la cua i que finalment genera una gràfica amb els resultats.
