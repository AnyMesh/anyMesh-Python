import json
from twisted.internet import reactor, error
from connections import MeshFactory, MeshTcpProtocol
from discovery import MeshUdpProtocol


class MeshDeviceInfo:
    def __init__(self, name, listens_to):
        self.name = name
        self.listens_to = listens_to


class MeshMessage:
    def __init__(self, sender, target, msg_type, data):
        self.sender = sender
        self.target = target
        self.type = msg_type
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
    MSG_TYPE_REQUEST = 0
    MSG_TYPE_PUBLISH = 1
    MSG_TYPE_SYSTEM = 2
    MSG_SYSTYPE_SUBSCRIPTIONS = 0


    def __init__(self, name, subscriptions, delegate, network_id="anymesh", udp_port=12345, tcp_port=12346):
        self.name = name
        self.subscriptions = subscriptions
        self.connections = []

        self.network_id = network_id
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.delegate = delegate

        #self.udp.setup()
        self.setup_tcp()



    def setup_tcp(self):
        f = MeshFactory(self)
        f.protocol = MeshTcpProtocol
        try:
            reactor.listenTCP(self.anymesh.tcp_port, f)
        except error.CannotListenError:
            self.anymesh.tcp_port += 1
            self.setup()
        else:
            self.anymesh._listening_at(self.anymesh.tcp_port)

    def setup_udp(self):
        reactor.listenMulticast(self.udp_port, MeshUdpProtocol(self), listenMultiple=True)

    @staticmethod
    def run():
        reactor.run()

    def get_connections(self):
        active_connections = []
        for connection in self.tcp.connections:
            if hasattr(connection, 'name'):
                active_connections.append(MeshDeviceInfo(connection.name[:], connection.listens_to[:]))
        return active_connections

    def publish(self, target, message):
        self.tcp.publish(target, message)

    def request(self, target, message):
        self.tcp.request(target, message)

    def _report(self, report_msg):
        self._received_msg({'sender': "diag", 'type': AnyMesh.MSG_TYPE_SYSTEM, 'target': 'report', 'data': {'msg': report_msg}})

    #From UDP:
    def _connect_to(self, address, port, name):
        self.tcp.connect(address, port, name)

    #From TCP:
    def _connected_to(self, connection):
        if hasattr(connection, 'name'):
            self.delegate.connected_to(MeshDeviceInfo(connection.name[:], connection.listens_to[:]))

    def _disconnected_from(self, connection):
        if hasattr(connection, 'name'):
            self.delegate.disconnected_from(connection.name[:])

    def _received_msg(self, data):
        msg = MeshMessage(data['sender'], data['target'], data['type'], data['data'])
        self.delegate.received_msg(msg)

    def _listening_at(self, server_port):
        self.udp.server_port = server_port

