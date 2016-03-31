from geosquizzy.socket.gs_socket import GsSocket
from geosquizzy.socket.utils import pre_data_bytes_stream

from socket import error
from socket import AF_INET, SOCK_STREAM
import random


class GsSocketClient(GsSocket):

    def __init__(self, *args, **kwargs):
        super(GsSocketClient, self).__init__(self, *args, **kwargs)
        self.__create_socket__()

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
        except (error,) as err:
            print(err)

    def disconnect(self):
        self.socket.close()

    def write(self, data):
        converted = pre_data_bytes_stream(data)
        self.socket.send(converted)


if __name__ == "__main__":
    import time
    client = GsSocketClient(HOST='localhost',
                            PORT=7801,
                            FAMILY=AF_INET,
                            TYPE=SOCK_STREAM)
    client.connect()
    while True:
        client.write(random.random())
        time.sleep(3)
    client.disconnect()