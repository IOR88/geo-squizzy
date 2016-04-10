#!/usr/bin/env python3.3.6

import unittest
import sys
import threading
import time

from socket import AF_INET, SOCK_STREAM

from geosquizzy.gs_socket.gs_socket import GsSocket
from geosquizzy.gs_socket.gs_server import GsSocketServer
from geosquizzy.gs_socket.gs_client import GsSocketClient


class SocketInitializationTest(unittest.TestCase):
    """
    Testing socket initialization process
    """
    def setUp(self):
        self.options = {'HOST': 'localhost',
                        'PORT': 8030,
                        'FAMILY': AF_INET,
                        'TYPE': SOCK_STREAM}
        self.socket = None

    def tearDown(self):
        self.socket.__close_socket__()

    def test_init_socket(self):
        """
        Testing Main Wrapper GsSocket Class Initialization and socket creation
        """
        self.socket = GsSocket(**self.options)
        self.socket.__create_socket__()


class SocketServerClientConnectionTest(unittest.TestCase):
    """
    Testing server/client write <-> read interactions
    """
    def setUp(self):
        self.options = {'HOST': 'localhost',
                        'PORT': 8030,
                        'FAMILY': AF_INET,
                        'TYPE': SOCK_STREAM,
                        'CONNECTIONS': 2}
        self.socket_server = GsSocketServer(**self.options)
        self.socket_client = GsSocketClient(**self.options)

    def tearDown(self):
        # self.socket_server.disconnect()
        pass
        # kill server_socket
        # tcpkill read ->

    def test_bind_socket(self):
        """
        Create Two sockets server and client, bind and connect them to the same port, triggering
        Write/Read talks and shutdown/close them
        """
        self.socket_server.create_connection()
        server_thread = threading.Thread(target=self.socket_server.run)
        server_thread.daemon = True
        server_thread.start()
        """
        Small timeout is needed here (could be caused by Thread not executed run function when client.connect()
        is called)
        """
        time.sleep(0.5)
        self.socket_client.connect()

        def __messaging__(socket, message):
            """
            :param socket: socket client
            :param message: 'TEST'+int()
            :return: Bool(message==res)
            """
            socket.write(message)
            res = socket.read(1024)
            if res:
                return message == str(res, 'utf-8')

        [self.assertTrue(__messaging__(self.socket_client, 'TEST'+str(x))) for x in range(0, 1000, 1)]
        self.socket_client.disconnect()


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')