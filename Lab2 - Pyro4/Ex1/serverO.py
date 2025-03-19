import Pyro4

@Pyro4.expose
class EchoServer():
    def echo(self,mss):
        print(mss)
        return f'Missatge enviat: {mss}'

daemon = Pyro4.Daemon(host='192.168.6.37')
ns = Pyro4.locateNS(host='192.168.6.37', port=9090)
uri = daemon.register(EchoServer)
ns.register('elnegro', uri)
daemon.requestLoop()