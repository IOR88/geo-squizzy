from geosquizzy.socket.gs_socket import GsSocket
from geosquizzy.socket.utils import pre_data_bytes_stream

from socket import error
from socket import AF_INET, SOCK_STREAM
import random


class GsSocketClient(GsSocket):

    def __init__(self, *args, **kwargs):
        super(GsSocketClient, self).__init__(self, *args, **kwargs)
        self.__create_socket__()
        # self.connect()

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
        except (error,) as err:
            print(err)

    def disconnect(self):
        self.__close_socket__()

    def write(self, data):
        # TODO do we have to connect each time ?
        # self.__create_socket__()
        # self.connect()
        try:
            converted = pre_data_bytes_stream(data)
            self.socket.send(converted)
            print('SENDED ?')
        except (Exception,) as err:
            print(err)
            assert False
        finally:
            # self.disconnect()
            pass

if __name__ == "__main__":
    # TODO TESTING
    client = GsSocketClient(HOST='localhost',
                            PORT=8030,
                            FAMILY=AF_INET,
                            TYPE=SOCK_STREAM)
    client.__create_socket__()
    client.connect()
    # while True:
    #     client.write(random.random())
    #     time.sleep(3)
    # client.disconnect()
    while True:
        data = client.socket.recv(1024)
        if data:
            print('DATA FROM DEMON', data)
        else:
            pass