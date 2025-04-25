import Pyro4
import random
import time

message_list = [
    "Eres un idiota, no sabes ni sumar.",
    "Vaya inútil estás hecho.",
    "Solo un tonto haría eso.",
    "Qué imbécil, de verdad.",
    "Menudo patán, siempre la lías.",
    "No seas pesado, cállate ya.",
    "¿Siempre tienes que ser tan torpe?",
    "Qué payaso, deja de molestar.",
    "No me hables, eres un estúpido.",
    "Pareces un niño malcriado."
]

daemon = Pyro4.Daemon(host='localhost')
ns = Pyro4.locateNS(host='localhost', port=9090)
uri = ns.lookup('insult.filter')
filter = Pyro4.Proxy(uri)

while True:
    filter.add_petitions(random.choice(message_list))
    time.sleep(5)