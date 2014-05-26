from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver


class MeshTcpProtocol(LineReceiver):
    def __init__(self, tcp_port):
        self.tcp_port = tcp_port

    def lineReceived(self, data):
        print "placeholder"

    def connectionMade(self):
        print "connection made"

    def connectionLost(self, reason):
        print "connection lost"

class MeshTcp:
    def __init__(self, tcp_port):
        self.tcp_port = tcp_port
        self.connections = []   #connected Twisted Factory objects (implementations of the protocol)

    def setup(self):
        f = Factory()
        f.protocol = MeshTcpProtocol(self.tcp_port)
        reactor.listenTCP(self.tcp_port, f)

    def connect(self, address):
        print "tcp connect"