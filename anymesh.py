from twisted.internet import protocol, reactor, task
from twisted.internet.protocol import DatagramProtocol
from twisted.protocols import basic
from mesh_tcp import MeshTcp
from mesh_udp import MeshUdp

def main():
    AnyMesh('dave', ['global', 'status'])

class AnyMesh:
    def __init__(self, name, listens_to, network_id="c8m3!x", udp_port=12345, tcp_port=12346):
        self.name = name
        self.listens_to = listens_to
        self.network_id = network_id
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.udp = MeshUdp(self)
        self.tcp = MeshTcp(self)
        self.udp.setup()
        self.tcp.setup()

        reactor.run()

    #From UDP:
    def connectTo(self, address):
        self.tcp.connect(address)


    #From TCP:
    def connectedTo(self, connection):
        print "from anymesh, connected"
        pass
    def disconnectedFrom(self, connection):
        pass

if __name__ == "__main__":
    main()