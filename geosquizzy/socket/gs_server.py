from geosquizzy.socket.gs_socket import GsSocket

from socket import error
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys


class GsSocketServer(GsSocket):

    def __init__(self, *args, **kwargs):
        GsSocket.__init__(self, *args, **kwargs)
        self.clients = set()
        self.__create_socket__()

    def disconnect(self):
        self.__close_socket__()

    def create_connection(self):
        try:
            self.socket.bind((self.HOST, self.PORT))
            # self.socket.listen(self.CONNECTIONS)
        except (error,) as err:
            print(err)
            sys.exit(1)

    def __broadcast__(self, data):
        for client in self.clients:
            try:
                client.sendall(data)
            except (BrokenPipeError, ConnectionResetError) as err:
                print(err)

    def __handle_client_req__(self, conn):
        while True:
                try:
                    data = conn.recv(1024)
                    if data:
                        print(str(data, 'utf-8'), '\n \n')
                        self.__broadcast__(data)
                    else:
                        print('closing connection ?')
                        conn.close()
                        self.clients.difference_update([conn])
                        break
                except (BrokenPipeError, ConnectionResetError) as err:
                    conn.close()
                    self.clients.difference_update([conn])
                    break

    def run(self):
        self.socket.listen(self.CONNECTIONS)

        while True:
            print('waiting for connection')
            conn, address = self.socket.accept()
            # self.clients.add(conn)
            print('Connected to address ', address, '\n')
            self.clients.add(conn)
            # TODO does socket.accept() can take some information ?
            # TODO if so then starting thread would be not needed,
            # TODO because we have only one client for reading from and only one
            # TODO client to whom we write
            Thread(target=self.__handle_client_req__, args=(conn,)).start()

    def kill(self):
        pass

if __name__ == "__main__":
    # TODO TESTING
    server = GsSocketServer(HOST='localhost',
                            PORT=8030,
                            FAMILY=AF_INET,
                            TYPE=SOCK_STREAM,
                            CONNECTIONS=10)
    server.create_connection()
    server.run()