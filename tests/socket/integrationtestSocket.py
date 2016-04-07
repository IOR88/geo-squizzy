#!/usr/bin/env python3.3.6

import unittest
import sys

from socket import AF_INET, SOCK_STREAM

from geosquizzy.socket.gs_client import GsSocketClient


class SocketClientServerConnectionTest(unittest.TestCase):
    """
    TEST for interaction between two client/one client and server during geo-squizzzy run function and
    where one is a default case for geo-squizzy and two would be when second client listen to demon broadcasting

    """
    def setUp(self):
        self.client_options = {'HOST': 'localhost',
                               'PORT': 8030,
                               'FAMILY': AF_INET,
                               'TYPE': SOCK_STREAM}
        self.socket_client = GsSocketClient(**self.client_options)

    def tearDown(self):
        self.socket_client.disconnect()

    def test_init_socket(self):
        pass


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')