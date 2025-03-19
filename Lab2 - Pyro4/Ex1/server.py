import Pyro4
import EchoServer

@Pyro4.expose
class EchoServer():
    def echo(self,mss):
        print(mss)
        return f'Missatge enviat: {mss}'

if __name__ == '__main__':
    daemon = Pyro4.Daemon()     #Especificar ip host    
    ns = Pyro4.locateNS()       #Especificar ip host i port
    uri = daemon.register(EchoServer)
    ns.register('echo.server', uri)
    daemon.requestLoop()