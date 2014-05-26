from socket import *
import socket
from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol
from anymesh import connectTo

class MeshUdpProtocol(DatagramProtocol):
    def __init__(self, network_id, udp_port):
        self.network_id = network_id
        self.udp_port = udp_port
    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        localhost = socket.gethostbyname(socket.gethostname())
        if data == self.network_id:
            connectTo(host)

    def startProtocol(self):
        print "protocol started"
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        l = task.LoopingCall(self.broadcast_function)
        l.start(2.0)

    def broadcast_function(self):
        self.transport.write(self.network_id, ('<broadcast>', self.udp_port))


class MeshUdp:
    def __init__(self, network_id, udp_port):
        self.network_id = network_id
        self.udp_port = udp_port


    def setup(self):
        reactor.listenUDP(self.udp_port, MeshUdpProtocol(self.network_id, self.udp_port))