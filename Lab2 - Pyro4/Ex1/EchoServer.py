import Pyro4

@Pyro4.expose
class EchoServer():
    def echo(mss):
        print(mss)