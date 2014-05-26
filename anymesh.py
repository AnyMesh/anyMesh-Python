from twisted.internet import protocol, reactor, task
from twisted.internet.protocol import DatagramProtocol
from twisted.protocols import basic
from mesh_tcp import MeshTcp
from mesh_udp import MeshUdp

def main():

    global udp, tcp

    udp = MeshUdp("c8m3!x", 12345)
    tcp = MeshTcp(12346)
    udp.setup()
    tcp.setup()

    reactor.run()

def connectTo(address):
    global tcp
    tcp.connect(address)

if __name__ == "__main__":
    main()