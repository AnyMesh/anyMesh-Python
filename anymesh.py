import json
from twisted.internet import reactor
from mesh_tcp import MeshTcp
from mesh_udp import MeshUdp

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
    def connected_to(self, device_info):
        print "connected to " + device_info.name
    def disconnected_from(self, name):
        print "disconnected from " + name
    def received_msg(self, message):
        print "received message from " + message.sender
        print "message body: " + json.dumps(message.data)


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
    def run(self):
        reactor.run()

    def get_connections(self):
        active_connections = []
        for connection in self.tcp.connections:
            if hasattr(connection, 'name'):
                active_connections.append(MeshDeviceInfo(connection.name, connection.listens_to))
        return active_connections[:]

    def publish(self, target, message):
        self.tcp.publish(target, message)
    def request(self, target, message):
        self.tcp.request(target, message)

    #From UDP:
    def _connect_to(self, address):
        self.tcp.connect(address)

    #From TCP:
    def _connected_to(self, connection):
        if hasattr(connection, 'name'):
            self.delegate.connected_to(MeshDeviceInfo(connection.name, connection.listens_to))

    def _disconnected_from(self, connection):
        if hasattr(connection, 'name'):
            self.delegate.disconnected_from(connection.name)

    def _received_msg(self, data):
        msg = MeshMessage(data['sender'], data['target'], data['type'], data['data'])
        self.delegate.received_msg(msg)




if __name__ == "__main__":
    AnyMesh('dave', ['global', 'status'], AnyMeshDelegateProtocol())
    reactor.run()