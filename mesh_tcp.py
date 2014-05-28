import json
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Factory
from twisted.protocols.basic import LineReceiver


class MeshTcpProtocol(LineReceiver):
    def __init__(self, mesh_tcp):
        self.mesh_tcp = mesh_tcp
        self.anymesh = self.mesh_tcp.anymesh
        self.name = None
        self.listens_to = []

    def lineReceived(self, data):
        print data
        msgObj = json.loads(data)
        if msgObj['type'] == 'info':
            self.name = msgObj['sender']
            self.listens_to = msgObj['listensTo']
            self.anymesh.connectedTo(self)

    def connectionMade(self):
        print "making connection"
        self.mesh_tcp.connections.append(self)
        self.sendInfo()

    def connectionLost(self, reason):
        print "connection lost"
        self.mesh_tcp.connections.remove(self)

    def sendInfo(self):
        infoObj = {'type': 'info', 'sender': self.anymesh.name, 'listensTo': self.anymesh.listens_to}
        self.sendLine(json.dumps(infoObj))

class MeshClientFactory(ClientFactory):
    protocol = MeshTcpProtocol

    def clientConnectionFailed(self, connector, reason):
        pass

    def clientConnectionLost(self, connector, reason):
        pass



class MeshTcp:
    def __init__(self, anymesh):
        self.anymesh = anymesh
        self.connections = []

    def setup(self):
        f = Factory()
        f.protocol = MeshTcpProtocol(self)
        reactor.listenTCP(self.anymesh.tcp_port, f)

    def connect(self, address):
        if not self.connectionExists(address):
            reactor.connectTCP(address, self.anymesh.tcp_port, MeshClientFactory())


#utility methods:
    def connectionExists(self, ipAddress):
        for connection in self.connections:
            if connection.transport.getHost() == ipAddress:
                return True
        return False
