from anymesh import AnyMesh, AnyMeshDelegateProtocol


import unittest

class TestAnyMeshBasic(unittest.TestCase):

    class LeftDelegate(AnyMeshDelegateProtocol):
        def connected_to(self, device_info):
            pass
        def disconnected_from(self, name):
            pass
        def received_msg(self, message):
            pass

    class RightDelegate(AnyMeshDelegateProtocol):
        def connected_to(self, device_info):
            pass
        def disconnected_from(self, name):
            pass
        def received_msg(self, message):
            pass

    def test_connect(self):
        self.leftMesh = AnyMesh('left', ['stuff', 'things'], TestAnyMeshBasic.LeftDelegate(), )



'''
    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)
            '''

if __name__ == '__main__':
    unittest.main()
