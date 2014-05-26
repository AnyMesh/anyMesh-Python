from twisted.internet import protocol, reactor, task
from twisted.internet.protocol import DatagramProtocol
from twisted.protocols import basic
from mesh_tcp import MeshTcp
from mesh_udp import MeshUdp

def main():
    AnyMesh()

class AnyMesh:
    def __init__(self):
        self.udp = MeshUdp(self, "c8m3!x", 12345)
        self.tcp = MeshTcp(12346)
        self.udp.setup()
        self.tcp.setup()

        reactor.run()

    def connectTo(self, address):
        self.tcp.connect(address)

if __name__ == "__main__":
    main()