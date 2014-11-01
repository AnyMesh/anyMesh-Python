import json
from socket import *
import socket
from twisted.internet import reactor, task
from twisted.internet.protocol import ClientFactory, ServerFactory, DatagramProtocol
from twisted.protocols.basic import LineReceiver



class MeshUdpProtocol(DatagramProtocol):
    def __init__(self, anymesh):
        self.network_id = anymesh.network_id
        self.udp_port = anymesh.udp_port

    def datagramReceived(self, data, (host, port)):
        if self.mesh_udp.server_port == 0:
            return
        data_array = data.split(',')
        msg_id = data_array[0]

        if msg_id == self.network_id:
            localhost = socket.gethostbyname(socket.gethostname())
            msg_port = int(data_array[1])
            msg_name = data_array[2]
            if (localhost != host and localhost != '127.0.1.1') or msg_port != self.mesh_udp.server_port:
                #self.mesh_udp.anymesh._report('udp', 'discovery says yes to connect')
                self.anymesh.connect_tcp(host, msg_port, msg_name)

    def startProtocol(self):
        #self.mesh_udp.anymesh._report('udp', 'starting protocol')
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        l = task.LoopingCall(self.broadcast_function)
        l.start(2.0)

    def broadcast_function(self):
        #self.mesh_udp.anymesh._report('udp', 'broadcasting on ' + str(self.mesh_udp.server_port))
        if self.anymesh.tcp_port == 0:
            return
        udp_msg = self.network_id + ',' + str(self.mesh_udp.server_port) + ',' + self.mesh_udp.anymesh.name
        self.transport.write(udp_msg, ('<broadcast>', self.udp_port))


class MeshTcpProtocol(LineReceiver):

    def lineReceived(self, data):
        connections = self.factory.mesh_tcp.connections
        msgObj = json.loads(data)
        if msgObj['type'] == 'info':
            self.factory.anymesh._report('tcp', 'client received info')
            #new - check array for duplicate - if ok, need to send PASS message to server
            existing_connection = self.factory.mesh_tcp.connection_for_name(msgObj['sender'])
            if existing_connection:
                existing_index = connections.index(existing_connection)
                this_index = connections.index(self)
                if this_index > existing_index:
                    self.factory.anymesh._report('tcp', 'throwing out based on index')
                    connections.remove(self)
                    self.transport.loseConnection()
                    return
            self.name = msgObj['sender']
            self.listens_to = msgObj['listensTo']
            self.sendPass()
            self.factory.anymesh._connected_to(self)
        else:
            self.factory.anymesh._received_msg(msgObj)

    def connectionMade(self):
        self.factory.mesh_tcp.connections.append(self)
        self.sendInfo()

    def connectionLost(self, reason):
        if self in self.factory.mesh_tcp.connections:
            self.factory.mesh_tcp.connections.remove(self)
        self.factory.anymesh._disconnected_from(self)

    def sendInfo(self):
        info_obj = self.factory.get_info_object()
        self.sendLine(json.dumps(info_obj))


class MeshClientFactory(ClientFactory):
    protocol = MeshTcpProtocol

    def __init__(self, anymesh):
        self.anymesh = anymesh

    def clientConnectionFailed(self, connector, reason):
        pass

    def clientConnectionLost(self, connector, reason):
        pass

    def get_info_object(self):
        return {'type': 'info', 'sender': self.anymesh.name, 'listensTo': self.anymesh.listens_to}


class MeshServerFactory(ServerFactory):
    protocol = MeshTcpProtocol

    def __init__(self, anymesh):
        self.anymesh = anymesh

    def get_info_object(self):
        return {'type': 'info', 'sender': self.anymesh.name, 'listensTo': self.anymesh.listens_to}