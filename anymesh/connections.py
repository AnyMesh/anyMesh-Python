import json
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.internet import error
from twisted.protocols.basic import LineReceiver


class MeshTcpProtocol(LineReceiver):

    def lineReceived(self, data):
        msgObj = json.loads(data)
        if msgObj['type'] == 'info':
            #self.factory.anymesh._report('tcp', 'client adding ' + msgObj['sender'])
            self.name = msgObj['sender']
            self.listens_to = msgObj['listensTo']
            self.factory.anymesh._connected_to(self)
        else:
            self.factory.anymesh._received_msg(msgObj)

    def connectionMade(self):
        self.factory.mesh_tcp.connections.append(self)


    def connectionLost(self, reason):
        if self in self.factory.mesh_tcp.connections:
            self.factory.mesh_tcp.connections.remove(self)
        self.factory.anymesh._disconnected_from(self)

    def sendInfo(self):
        infoObj = self.factory.getInfoObject()
        self.sendLine(json.dumps(infoObj))


class MeshTcpClientProtocol(MeshTcpProtocol):

    def connectionMade(self):
        self.factory.mesh_tcp.connections.append(self)
        self.sendInfo()


class MeshTcpServerProtocol(MeshTcpProtocol):
    def lineReceived(self, data):
        msgObj = json.loads(data)
        if msgObj['type'] == 'info':
            if not self.factory.mesh_tcp.connection_for_name(msgObj['sender']):
                #self.factory.anymesh._report('tcp', 'server adding ' + msgObj['sender'])
                self.name = msgObj['sender']
                self.listens_to = msgObj['listensTo']
                self.factory.anymesh._connected_to(self)
                self.sendInfo()
            else:
                self.factory.mesh_tcp.connections.remove(self)
                self.disconnect()
        else:
            self.factory.anymesh._received_msg(msgObj)


class MeshClientFactory(ClientFactory):
    protocol = MeshTcpClientProtocol

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
    protocol = MeshTcpServerProtocol

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
        f.protocol = MeshTcpServerProtocol
        try:
            reactor.listenTCP(self.anymesh.tcp_port, f)
        except error.CannotListenError:
            self.anymesh.tcp_port += 1
            self.setup()
        else:
            self.anymesh._listening_at(self.anymesh.tcp_port)


    def connect(self, address, port, name):
        if not self.connection_for_name(name):
            #self.anymesh._report('tcp', 'connecting now to ' + address + ',' + str(port) + ',' + name)
            reactor.connectTCP(address, port, MeshClientFactory(self))

    def request(self, target, message):
        msg_string = self.string_from_msg_data('req', target, message)
        conn = self.connection_for_name(target)
        if conn:
            self.connection_for_name(target).sendLine(msg_string)

    def publish(self, target, message):
        msg_string = self.string_from_msg_data('req', target, message)
        for connection in self.connections:
            for subscription in connection.listens_to:
                if subscription == target:
                    connection.sendLine(msg_string)
                    break

#utility methods:
    def string_from_msg_data(self, msg_type, target, payload):
        package = {"type": msg_type, "target": target, "sender": self.anymesh.name, "data": payload}
        return json.dumps(package)

    def connection_for_name(self, name):
        for connection in self.connections:
            if hasattr(connection, 'name'):
                if connection.name == name:
                    return connection
        return None