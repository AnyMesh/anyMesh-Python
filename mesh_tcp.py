import json
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.protocols.basic import LineReceiver


class MeshTcpProtocol(LineReceiver):

    def lineReceived(self, data):
        msgObj = json.loads(data)
        if msgObj['type'] == 'info':
            self.name = msgObj['sender']
            self.listens_to = msgObj['listensTo']
            self.factory.anymesh._connected_to(self)
        else:
            self.factory.anymesh._received_msg(msgObj)

    def connectionMade(self):
        self.factory.mesh_tcp.connections.append(self)
        self.sendInfo()

    def connectionLost(self, reason):
        self.factory.mesh_tcp.connections.remove(self)
        self.factory.anymesh._disconnected_from(self)

    def sendInfo(self):
        infoObj = self.factory.getInfoObject()
        self.sendLine(json.dumps(infoObj))

class MeshClientFactory(ClientFactory):
    protocol = MeshTcpProtocol

    def __init__(self, mesh_tcp):
        self.mesh_tcp = mesh_tcp
        self.anymesh = mesh_tcp.anymesh

    def clientConnectionFailed(self, connector, reason):
        pass

    def clientConnectionLost(self, connector, reason):
        pass

    def getInfoObject(self):
         return {'type': 'info', 'sender': self.anymesh.name, 'listensTo': self.anymesh.listens_to}

class MeshServerFactory(ServerFactory):
    protocol = MeshTcpProtocol

    def __init__(self, mesh_tcp):
        self.mesh_tcp = mesh_tcp
        self.anymesh = mesh_tcp.anymesh

    def getInfoObject(self):
         return {'type': 'info', 'sender': self.anymesh.name, 'listensTo': self.anymesh.listens_to}


class MeshTcp:
    def __init__(self, anymesh):
        self.anymesh = anymesh
        self.connections = []

    def setup(self):
        f = MeshServerFactory(self)
        f.protocol = MeshTcpProtocol
        reactor.listenTCP(self.anymesh.tcp_port, f)

    def connect(self, address):
        if not self.connectionExists(address):
            reactor.connectTCP(address, self.anymesh.tcp_port, MeshClientFactory(self))

    def request(self, target, message):
        msg_string = self.string_from_msg_data('req', target, message)
        for connection in self.connections:
            if connection.name == target:
                connection.sendLine(msg_string)
                return

    def publish(self, target, message):
        msg_string = self.string_from_msg_data('req', target, message)
        for connection in self.connections:
            for subscription in connection.listens_to:
                if subscription == target:
                    connection.sendLine(msg_string)
                    break


#utility methods:
    def connectionExists(self, ipAddress):
        for connection in self.connections:
            if connection.transport.getPeer().host == ipAddress:
                return True
        return False

    def string_from_msg_data(self, msg_type, target, payload):
        package = {"type": msg_type, "target": target, "sender": self.anymesh.name, "data": payload}
        return json.dumps(package)