import json
from socket import *
import socket
from twisted.internet import task
from twisted.internet.protocol import ClientFactory, ServerFactory, DatagramProtocol
from twisted.protocols.basic import LineReceiver


class MeshUdpProtocol(DatagramProtocol):
    def __init__(self, anymesh):
        self.anymesh = anymesh
        self.network_id = anymesh.network_id
        self.udp_port = anymesh.udp_port

    def datagramReceived(self, data, (host, port)):
        if self.anymesh.tcp_port == 0:
            return
        data_array = data.split(',')
        msg_id = data_array[0]

        if msg_id == self.network_id:
            localhost = socket.gethostbyname(socket.gethostname())
            msg_port = int(data_array[1])
            msg_name = data_array[2]
            if (localhost != host) or msg_port != self.anymesh.tcp_port:

                #check order of name
                if msg_name < self.anymesh.name:
                    self.anymesh.connect_tcp(host, msg_port, msg_name)

    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        l = task.LoopingCall(self.broadcast_function)
        l.start(2.0)

    def broadcast_function(self):
        if self.anymesh.tcp_port == 0:
            return
        udp_msg = self.network_id + ',' + str(self.anymesh.tcp_port) + ',' + self.anymesh.name
        self.transport.write(udp_msg, ('<broadcast>', self.udp_port))


class MeshTcpProtocol(LineReceiver):
    def __init__(self):
        self.name = None
        self.subscriptions = []

    def lineReceived(self, data):
        anymesh = self.factory.anymesh

        msgObj = json.loads(data)
        if msgObj['type'] == anymesh.MSG_TYPE_SYSTEM:
            sysData = msgObj['data']
            if sysData['type'] == anymesh.MSG_SYSTYPE_SUBSCRIPTIONS:
                self.subscriptions = sysData['subscriptions']

                if sysData['isUpdate']:
                    anymesh._updated_subscriptions(self.subscriptions, self.name)
                else:
                    self.name = msgObj['sender']
                    anymesh._connected_to(self)
        else:
            anymesh._received_msg(msgObj)

    def connectionMade(self):
        if not self in self.factory.anymesh.connections:
            self.factory.anymesh.connections.append(self)
            self.sendInfo(False)

    def connectionLost(self, reason):
        if self in self.factory.anymesh.connections:
            self.factory.anymesh.connections.remove(self)
            self.factory.anymesh._disconnected_from(self)

    def sendInfo(self, isUpdate):
        anymesh = self.factory.anymesh
        msg_obj = {'type': anymesh.MSG_SYSTYPE_SUBSCRIPTIONS, 'isUpdate': isUpdate, 'subscriptions': anymesh.subscriptions}
        info_obj = {'type': anymesh.MSG_TYPE_SYSTEM, 'sender': anymesh.name, 'target': self.name, 'data': msg_obj}
        self.sendLine(json.dumps(info_obj))


class MeshClientFactory(ClientFactory):
    protocol = MeshTcpProtocol

    def __init__(self, anymesh):
        self.anymesh = anymesh

    def clientConnectionFailed(self, connector, reason):
        pass

    def clientConnectionLost(self, connector, reason):
        pass


class MeshServerFactory(ServerFactory):
    protocol = MeshTcpProtocol

    def __init__(self, anymesh):
        self.anymesh = anymesh