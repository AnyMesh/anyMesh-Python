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
        localhost = socket.gethostbyname(socket.gethostname())
        if data == self.network_id and localhost != host and localhost != "127.0.1.1":
            self.mesh_udp.anymesh._connect_to(host)
            pass

    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        l = task.LoopingCall(self.broadcast_function)
        l.start(2.0)

    def broadcast_function(self):
        self.transport.write(self.network_id, ('<broadcast>', self.udp_port))


class MeshUdp:
    def __init__(self, anymesh):
        self.anymesh = anymesh
        self.network_id = anymesh.network_id
        self.udp_port = anymesh.udp_port


    def setup(self):
        reactor.listenUDP(self.udp_port, MeshUdpProtocol(self))