import unittest
from twisted.internet import reactor, task

class ReactorTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ReactorTestCase, self).__init__(*args, **kwargs)
        self.done = False

    def timeOutAfter(self, seconds):
        f = reactor.callLater(seconds, self.timedOut)
        f.start(seconds)

    def timedOut(self):
        self.done = True
        self.assertTrue(False, "test timed out!")
        print "Test Timed Out!"
        if reactor.running:
            reactor.stop()

    def reactorAssert(self, success, msg):
        if not self.done:
            self.assertTrue(success, msg)

    def reactorTestComplete(self):
        self.done = True
        self.assertTrue(True, "test complete!")
        print "Test Complete!"
        if reactor.running:
            reactor.stop()
