from geosquizzy.socket.gs_socket import GsSocket

from socket import error
import sys


class GsSocketServer(GsSocket):

    def __init__(self, *args, **kwargs):
        GsSocket.__init__(self, *args, **kwargs)
        self.__create_socket__()

    def disconnect(self):
        self.socket.close()

    def create_connection(self):
        try:
            self.socket.bind((self.HOST, self.PORT))
            self.socket.listen(self.CONNECTIONS)
        except (error,) as err:
            print(err)
            sys.exit(1)

    def listen(self):
        self.socket.listen(self.CONNECTIONS)

        while True:
            conn, address = self.socket.accept()

            data = conn.recv(1024)
            if data:
                print('Connected to address ', address, '\n')
                print(str(data, 'utf-8'), '\n \n')
            else:
                self.socket.close()

    def kill(self):
        pass