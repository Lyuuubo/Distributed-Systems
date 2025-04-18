Primer exercici (EX1):
    Coses importants:
    - Per permetre tot el mecanisme de Subscriptors, s'ha realitzat amb processos. Segons el sistema operatiu, els processo es gestionen diferents.
        -> Windows no permet serialitzar instàncies de multiprocessing.Manager().list() fora del main "if __name__ == '__main__'". En aquest cas aquestes llistes estan fora del main i no funciona. Llavors la funcionalitat de permetre enviar nous insults un cop activada la funció de notificar aels subscriptors, no es vàlida en windows.
        -> Linix, tot funciona correctament.

    Estructura:
    - Client.py
    - InitialClient.py
    - InsultServiceLinux.py
    - InsultServiceWindows.py
    - s1,s2,s3.py

Segons exercici (EX2):
    Coses importants:
    - InsultFilter es un servei que disposa de funcions de consumidor i productor, en aquest cas, dintrem un client que estara continuament enviant feina a una cua interna del servei i un altre client que consumira continuament aquestes dades.
    - De moment, només ho estem tractant amb un únic node, llavors no necessitem una cua compartida com redis. Usem collections.deque.
    - Per el client, únicament tenim un fitxer on es pot sel·leccionar que es vol fer.

    Estructura:
    - ClientInsult.py
    - InsultFilter.py
    

