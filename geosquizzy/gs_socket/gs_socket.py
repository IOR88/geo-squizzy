from socket import socket, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR, SHUT_WR

# http://man7.org/linux/man-pages/man7/socket.7.html -> Signals


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
            """
            SO_REUSEADDR ->
            This socket option tells the kernel that even if this port is busy (in
            the TIME_WAIT state), go ahead and reuse it anyway.  If it is busy,
            but with another state, you will still get an address already in use
            error.  It is useful if your server has been shut down, and then
            restarted right away while sockets are still active on its port.  You
            should be aware that if any unexpected data comes in, it may confuse
            your server, but while this is possible, it is not likely.
            """
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def __close_socket__(self):
        """
        http://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close/598759#598759

        Calling close and shutdown have two different effects on the underlying socket.

        The first thing to point out is that the socket is a resource in the underlying OS
        and multiple processes can have a handle for the same underlying socket.
        When you call close it decrements the handle count by one and if the handle count has reached zero
        then the socket and associated connection goes through the normal close procedure
        (effectively sending a FIN / EOF to the peer) and the socket is deallocated.

        The thing to pay attention to here is that if the handle count does not reach zero because
        another process still has a handle to the socket then the connection is not closed
        and the socket is not deallocated.

        On the other hand calling shutdown for reading and writing closes the underlying connection and
        sends a FIN / EOF to the peer regardless of how many processes have handles to the socket.

        However, it does not deallocate the socket and you still need to call close afterward.

        """
        try:
            """
            Break the connection
            for writing, The server socket will detect EOF now.
            Note: reading from the socket is still allowed.
            The server may send some more data
            after receiving EOF, why not?
            """
            self.socket.shutdown(SHUT_WR)
        except (OSError,) as err:
            pass
        self.socket.close()