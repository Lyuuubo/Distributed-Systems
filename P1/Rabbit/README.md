Primer exercici (EX1):
    Coses importants:
    - Per fer-ho, tindrem una cua on el client i el servidor es conectaràn. 
    - Segons el valor que li passi el client per la cua, el servidor realitzarà alguna funció o un altra.
    - En cas de no ser cap valor conegut, significa que es un insurt i es posarà dintre de la llista d'insults.
    - ELs mètodes d'activar i parar broadcast i afegir insults, es realitzaràn sense retornar res a l'usuari. EN cas de la funció get instult, es realitzarà de forma asíncrona, guardant l'insult a la llista que l'usuari ens defineixi. Aquest procés es realitzarà de forma asíncrona.

    Estructura:
    ClientService.py
    InsultService.py
    Subscriber.py

Segon exercici (EX2):
    Coses importants:
    - Per realitzar aquesta tasca, els missatges filtrats es guardaràn a una llista de Redis.

    Estructura:
    InsultFilter.py
    TextProducer.py
    AngryProducer.py
    CheckResultList.py
    Extra: DeleteRedisList.py



