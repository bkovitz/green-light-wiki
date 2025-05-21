from teest import *
from Misc import forceRemove

from SocketServer import SocketServer
import socket

from WikiClient import socketTransaction

socketFilename = "wiki.test.socket"


class ut_SocketServer:

    def __init__(self):
        self.serviceGotException = False

    def setUp(self):
        forceRemove(socketFilename)

    def tearDown(self):
        forceRemove(socketFilename)

    def testSocketService(self):
        def mockService(environ, stdin):
            try:
                result = environ["STRING"] + "\n" + stdin.read()
                return result
            except Exception as e:
                self.serviceGotException = e

        server = SocketServer(socketFilename, mockService)

        s = "transaction\nSTRING=this=string\n\ntwo lines\nof stdin\n"

        expect = """this=string
two lines
of stdin
"""
        got = socketTransaction(socketFilename, s)
        TEST_EQ(expect, got)
        TEST_EQ(False, self.serviceGotException)

        TEST(server.isAlive())

        got = socketTransaction(socketFilename, s)
        TEST_EQ(expect, got)
        TEST_EQ(False, self.serviceGotException)

        TEST(server.isAlive())

        server.terminate()
        TEST(not server.isAlive())
        TEST_EQ(False, self.serviceGotException)

    def testInvalidEnvironment(self):
        def mockService(environ, stdin):
            try:
                result = environ["STRING"] + "\n" + stdin.read()
                return result
            except Exception as e:
                self.serviceGotException = e
                return ""

        server = SocketServer(socketFilename, mockService)

        s = "transaction\ninvalid environment\n\ntwo lines\nof stdin\n"

        got = socketTransaction(socketFilename, s)
        TEST(self.serviceGotException)

        server.terminate()

    def testSameServiceTwice(self):
        def mockService(environ, stdin):
            return "mock data"

        # note same socketFilename for both servers
        server1 = SocketServer(socketFilename, mockService, timeout=0.5)
        server2 = SocketServer(socketFilename, mockService, timeout=0.5)

        server1.kill()
        server2.kill()
