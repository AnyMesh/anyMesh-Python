from socket import *
import socket
from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol


class MeshUdpProtocol(DatagramProtocol):
    def __init__(self, mesh_udp):
        self.mesh_udp = mesh_udp
        self.network_id = mesh_udp.network_id
        self.udp_port = mesh_udp.udp_port

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
                self.mesh_udp.anymesh._connect_to(host, msg_port, msg_name)

    def startProtocol(self):
        #self.mesh_udp.anymesh._report('udp', 'starting protocol')
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        l = task.LoopingCall(self.broadcast_function)
        l.start(2.0)

    def broadcast_function(self):
        #self.mesh_udp.anymesh._report('udp', 'broadcasting on ' + str(self.mesh_udp.server_port))
        if self.mesh_udp.server_port == 0:
            return
        udp_msg = self.network_id + ',' + str(self.mesh_udp.server_port) + ',' + self.mesh_udp.anymesh.name
        self.transport.write(udp_msg, ('<broadcast>', self.udp_port))


class MeshUdp:
    def __init__(self, anymesh):
        self.anymesh = anymesh
        self.network_id = anymesh.network_id
        self.udp_port = anymesh.udp_port
        self.server_port = 0


    def setup(self):
        reactor.listenMulticast(self.udp_port, MeshUdpProtocol(self), listenMultiple=True)