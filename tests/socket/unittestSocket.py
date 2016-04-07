#!/usr/bin/env python3.3.6

import unittest
import sys
import threading

from socket import AF_INET, SOCK_STREAM

from geosquizzy.socket.gs_socket import GsSocket
from geosquizzy.socket.gs_server import GsSocketServer
from geosquizzy.socket.gs_client import GsSocketClient


class SocketInitializationTest(unittest.TestCase):
    def setUp(self):
        self.options = {'HOST': 'localhost',
                        'PORT': 8030,
                        'FAMILY': AF_INET,
                        'TYPE': SOCK_STREAM}
        self.socket = None

    def tearDown(self):
        self.socket.__close_socket__()

    def test_init_socket(self):
        self.socket = GsSocket(**self.options)
        self.socket.__create_socket__()


class SocketServerClientConnectionTest(unittest.TestCase):
    def setUp(self):
        self.options = {'HOST': 'localhost',
                        'PORT': 8030,
                        'FAMILY': AF_INET,
                        'TYPE': SOCK_STREAM,
                        'CONNECTIONS': 2}
        self.socket_server = GsSocketServer(**self.options)
        self.socket_client = GsSocketClient(**self.options)

    def tearDown(self):
        self.socket_server.disconnect()
        self.socket_client.disconnect()

    def test_bind_socket(self):
        self.socket_server.create_connection()
        # threading.Thread(target=self.socket_server.run).start()
        # with self.socket_server.run() as m:
        #     self.socket_client.connect()
        #     pass
        # # self.socket_client.connect()
        # pass


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')