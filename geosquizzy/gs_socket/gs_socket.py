from socket import socket, SOL_SOCKET, SO_REUSEADDR


class GsSocket:
    def __init__(self, *args, **kwargs):
        self.HOST = kwargs.get('HOST', None)
        self.PORT = kwargs.get('PORT', None)
        self.FAMILY = kwargs.get('FAMILY', None)
        self.TYPE = kwargs.get('TYPE', None)
        self.CONNECTIONS = kwargs.get('CONNECTIONS', None)
        self.socket = None

    def __create_socket__(self, server=None):
        """
        :arg server Bool()
        """
        self.socket = socket(family=self.FAMILY, type=self.TYPE)
        if server:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def __close_socket__(self):
        self.socket.close()