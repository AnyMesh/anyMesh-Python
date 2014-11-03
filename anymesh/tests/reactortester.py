import unittest
from twisted.internet import reactor

class ReactorTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ReactorTestCase, self).__init__(*args, **kwargs)
        self.done = False

    def reactorAssertTrue(self, success, msg):
        if not self.done:
            self.assertTrue(success, msg)

    def test_done(self):
        self.done = True
        self.assertTrue(True, "test complete!")
        if reactor.running:
            reactor.stop()