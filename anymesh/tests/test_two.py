import sys
sys.path.append('../../')
from anymesh import AnyMesh, AnyMeshDelegateProtocol
import unittest
from twisted.internet import reactor

class TestAnyMeshBasic(unittest.TestCase, AnyMeshDelegateProtocol):
    connections = 0

    def connected_to(self, device_info):
            self.connections += 1
            if self.connections == 2:
                reactor.stop()

    def disconnected_from(self, name):
            pass
    def received_msg(self, message):
            pass


    def test_connect(self):
        self.leftMesh = AnyMesh('left', ['stuff', 'things'], self)
        self.rightMesh = AnyMesh('right', ['stuff', 'things'], self)

        AnyMesh.run()

        self.assertTrue(True, "Test done!")

if __name__ == '__main__':
    unittest.main()
