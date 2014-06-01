import json
from twisted.internet import reactor
from mesh_tcp import MeshTcp
from mesh_udp import MeshUdp


class AnyMesh:
    def __init__(self, name, listens_to, delegate, network_id="c8m3!x", udp_port=12345, tcp_port=12346):
        self.name = name
        self.listens_to = listens_to
        self.network_id = network_id
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.delegate = delegate
        self.udp = MeshUdp(self)
        self.tcp = MeshTcp(self)
        self.udp.setup()
        self.tcp.setup()


    #From UDP:
    def connectTo(self, address):
        self.tcp.connect(address)


    #From TCP:
    def connectedTo(self, connection):
        if connection.name != None:
            self.delegate.connectedTo(MeshDeviceInfo(connection.name, connection.listens_to))
    def disconnectedFrom(self, connection):
        if connection.name != None:
            self.delegate.disconnectedFrom(connection.name)
    def receivedMessage(self, data):
        msg = MeshMessage(data['sender'], data['target'], data['type'], data['data'])
        self.delegate.receivedMessage(msg)

class MeshDeviceInfo:
    def __init__(self, name, listens_to):
        self.name = name
        self.listens_to = listens_to

class MeshMessage:
    def __init__(self, sender, target, type, data):
        self.sender = sender
        self.target = target
        self.type = type
        self.data = data

class AnyMeshDelegateProtocol:
    def connectedTo(self, device_info):
        print "connected to " + device_info.name
    def disconnectedFrom(self, name):
        print "disconnected from " + name
    def receivedMessage(self, message):
        print "received message from " + message.sender
        print "message body: " + json.dumps(message.data)




if __name__ == "__main__":
    AnyMesh('dave', ['global', 'status'], AnyMeshDelegateProtocol())
    reactor.run()