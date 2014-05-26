from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Factory
from twisted.protocols.basic import LineReceiver


class MeshTcpProtocol(LineReceiver):
    def __init__(self, tcp_port):
        self.tcp_port = tcp_port
        self.name = None
        self.ipAddress = None
        self.listensTo = []

    def lineReceived(self, data):
        print "placeholder"

    def connectionMade(self):
        self.send_info()

    def connectionLost(self, reason):
        print "connection lost"

class MeshClientFactory(ClientFactory):
    protocol = MeshTcpProtocol

    def clientConnectionFailed(self, connector, reason):
        pass

    def clientConnectionLost(self, connector, reason):
        pass



class MeshTcp:
    def __init__(self, tcp_port):
        self.tcp_port = tcp_port
        self.connections = []

    def setup(self):
        f = Factory()
        f.protocol = MeshTcpProtocol(self.tcp_port)
        reactor.listenTCP(self.tcp_port, f)

    def connect(self, address):
        if not self.connectionExists(address):
            reactor.connectTCP(address, self.tcp_port, MeshClientFactory())


#utility methods:
    def connectionExists(self, ipAddress):
        for connection in self.connections:
            if connection.transport.getHost() == ipAddress:
                return True
        return False
