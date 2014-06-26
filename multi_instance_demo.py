import anymesh.core

class LeftDelegate(anymesh.core.AnyMeshDelegateProtocol):
    def connected_to(self, device_info):
        print('left connected to ' + device_info.name)

    def disconnected_from(self, name):
        pass

    def received_msg(self, message):
        print('left received message from ' + message.sender)
        print('message: ' + message.data['msg'])
        leftMesh.request('right', {'msg': 'back at ya righty!'})


class RightDelegate(anymesh.core.AnyMeshDelegateProtocol):
    def connected_to(self, device_info):
        print('right connected to ' + device_info.name)
        rightMesh.request('left', {'msg': 'hey lefty!'})

    def disconnected_from(self, name):
        pass

    def received_msg(self, message):
        print('right received message from ' + message.sender)
        print('message: ' + message.data['msg'])


leftMesh = anymesh.core.AnyMesh('left', 'global', LeftDelegate())

rightMesh = anymesh.core.AnyMesh('right', 'global', RightDelegate())

leftMesh.run()
