#!/usr/bin/env python3.3.6

import unittest
import sys
import threading
import queue
import time

from socket import AF_INET, SOCK_STREAM

from geosquizzy.gs_socket.gs_client import GsSocketClient
from geosquizzy.gs_socket.gs_server import GsSocketServer
from geosquizzy.geosquizzy import GeoSquizzy

from tests.getdata import get_geojson


class SocketClientServerConnectionTest(unittest.TestCase):
    """
    Testing interactions between server/clients during geosquizzy algorithm execution
    """
    def setUp(self):
        self.socket_options = {'HOST': 'localhost',
                               'PORT': 8030,
                               'FAMILY': AF_INET,
                               'TYPE': SOCK_STREAM,
                               'CONNECTIONS': 2}
        self.socket_client = GsSocketClient(**self.socket_options)
        self.socket_server = GsSocketServer(**self.socket_options)

        self.geojson_options = {'geojson_options': {'mode': 'static', 'geojson_type': 'FeatureCollection'},
                                'outcome_options': {},
                                'optim': {'batch': 1, 'loss': -5.0}
                                }
        self.data = get_geojson(path="/home/ing/PycharmProjects/geo-squizzy/"
                                     "geosquizzy/build_big_data/data/dump1000.json")

    def tearDown(self):
        pass

    def test_geosquizzy_sockets(self):
        """
        It testing listening to messages broadcasted by socket server(which receive it from geosquizzy algorithm
        client) by another client
        """

        # Starting server thread
        self.socket_server.create_connection()

        server_thread = threading.Thread(target=self.socket_server.run)
        server_thread.daemon = True
        server_thread.start()

        second_client_data = queue.Queue()

        def second_client_listen(client, q):
            while True:
                data = client.read(1024)
                if data:
                    q.put(str(data, 'utf-8'))
                    q.task_done()
                else:
                    break

        time.sleep(0.5)

        # Starting second client thread
        self.socket_client.connect()
        second_client_thread = threading.Thread(target=second_client_listen,
                                                args=(self.socket_client, second_client_data))
        second_client_thread.start()

        # Starting geosquizzy socket client and algorithm execution
        self.geosquizzy = GeoSquizzy(**self.geojson_options)
        self.geosquizzy.start(geojson=self.data)

        # self.socket_client.disconnect()
        time.sleep(0.5)
        self.socket_client.disconnect()

        # Waiting for second_client to receive all data
        second_client_thread.join()

        # Waiting for second_client data
        second_client_data.join()

        # Getting second client
        second_client_res = []
        while True:
            if not second_client_data.empty():
                val = second_client_data.get()
                second_client_res.append(val)
            else:
                break
        # Getting geosquizzy result
        geosquizzy_res = self.geosquizzy.get_results()

        # Compare test
        # print(second_client_res)
        # print(geosquizzy_res)
        # a = set(geosquizzy_res)
        # print(a)


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')