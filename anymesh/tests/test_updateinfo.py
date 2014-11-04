import sys
import unittest
sys.path.append('../../')
from anymesh import AnyMesh, AnyMeshDelegateProtocol
from reactortester import ReactorTestCase

class TestUpdatingInfo(ReactorTestCase, AnyMeshDelegateProtocol):
    connections = 0

    def connected_to(self, anymesh, device_info):
            print "connection detected!"
            self.connections += 1
            if self.connections > 2:
                self.reactorAssert(False, "only 2 connections in this test!")
            if device_info.name == "receiver":
                self.sender.publish('stuff', {'index':1})

    def disconnected_from(self, anymesh, name):
            self.reactorAssert(False, "no disconnecting in this test!")
    def received_msg(self, anymesh, message):
            if message.data['index'] == 1:
                self.receiver.update_subscriptions(['end'])
            elif message.data['index'] == 2:
                print "received msg for end keyword"
                self.reactorTestComplete()
    def received_updated_subscriptions(self, anymesh, subscriptions, name):
            self.sender.publish('end', {'index':2})

    def test_connect(self):
        self.sender = AnyMesh('sender', ['stuff', 'things'], self)
        self.receiver = AnyMesh('receiver', ['stuff', 'things'], self)
        AnyMesh.run()



if __name__ == '__main__':
    unittest.main()
