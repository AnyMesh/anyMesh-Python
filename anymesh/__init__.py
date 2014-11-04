import json
from twisted.internet import reactor, error
from connections import MeshClientFactory, MeshServerFactory, MeshTcpProtocol, MeshUdpProtocol


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
    def connected_to(self, anymesh, device_info):
        pass
    def disconnected_from(self, anymesh, name):
        pass
    def received_msg(self, anymesh, message):
        pass
    def received_updated_subscriptions(self, anymesh, subscriptions, name):
        pass

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
        self.tcp_port = 0
        self.udp_port = udp_port
        self.working_port = tcp_port
        self.delegate = delegate

        self.setup_udp()
        self.setup_tcp()

    def setup_tcp(self):
        f = MeshServerFactory(self)
        f.protocol = MeshTcpProtocol
        try:
            reactor.listenTCP(self.working_port, f)
        except error.CannotListenError:
            self.working_port += 1
            self.setup_tcp()
        else:
            self.tcp_port = self.working_port

    def setup_udp(self):
        reactor.listenMulticast(self.udp_port, MeshUdpProtocol(self), listenMultiple=True)

    @staticmethod
    def run():
        reactor.run()

    def connect_tcp(self, address, port, name):
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
            for subscription in connection.subscriptions:
                if subscription == target:
                    connection.sendLine(msg_string)
                    break
    def update_subscriptions(self, subscriptions):
        self.subscriptions = subscriptions
        for connection in self.connections:
            connection.sendInfo(True)

#utility methods:
    def string_from_msg_data(self, msg_type, target, payload):
        package = {"type": msg_type, "target": target, "sender": self.name, "data": payload}
        return json.dumps(package)

    def connection_for_name(self, name):
        for connection in self.connections:
            if hasattr(connection, 'name'):
                if connection.name == name:
                    return connection
        return None

    def get_connections(self):
        active_connections = []
        for connection in self.connections:
            if hasattr(connection, 'name'):
                active_connections.append(MeshDeviceInfo(connection.name[:], connection.subscriptions[:]))
        return active_connections

    def _report(self, report_msg):
        self._received_msg({'sender': "diag", 'type': AnyMesh.MSG_TYPE_SYSTEM, 'target': 'report', 'data': {'msg': report_msg}})

#From TCP:
    def _connected_to(self, connection):
        if hasattr(connection, 'name'):
            self.delegate.connected_to(self, MeshDeviceInfo(connection.name[:], connection.subscriptions[:]))

    def _disconnected_from(self, connection):
        if hasattr(connection, 'name'):
           self.delegate.disconnected_from(self, connection.name[:])

    def _received_msg(self, data):
        msg = MeshMessage(data['sender'], data['target'], data['type'], data['data'])
        self.delegate.received_msg(self, msg)
    def _updated_subscriptions(self, subscriptions, name):
        self.delegate.received_updated_subscriptions(self, subscriptions, name)