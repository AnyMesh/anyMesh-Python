from anymesh import AnyMesh, AnyMeshDelegateProtocol

class LeftDelegate(AnyMeshDelegateProtocol):
    def connected_to(self, device_info):
        print('left connected to ' + device_info.name)

    def disconnected_from(self, name):
        pass

    def received_msg(self, message):
        print('left received message from ' + message.sender)
        print('message: ' + message.data['msg'])
        leftMesh.request('right', {'msg': 'back at ya righty!'})


class RightDelegate(AnyMeshDelegateProtocol):
    def connected_to(self, device_info):
        print('right connected to ' + device_info.name)
        rightMesh.request('left', {'msg': 'hey lefty!'})

    def disconnected_from(self, name):
        pass

    def received_msg(self, message):
        print('right received message from ' + message.sender)
        print('message: ' + message.data['msg'])


leftMesh =AnyMesh('left', 'global', LeftDelegate())

rightMesh = AnyMesh('right', 'global', RightDelegate())

AnyMesh.run()
