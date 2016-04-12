import sys
import os
import time
import atexit
from signal import SIGTERM
from socket import error

from geosquizzy.gs_socket.gs_server import GsSocketServer


# http://www.python.rk.edu.pl/w/p/python-i-programowanie-sieciowe/
# http://www.python.rk.edu.pl/w/p/proste-demony-uniksowe-w-pythonie/
# http://code.activestate.com/recipes/278731-creating-a-daemon-the-python-way/
# http://web.archive.org/web/20131017130434/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

class Demon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, *args, **kwargs):
        self.std_in = kwargs.get('std_in', '/dev/null')
        self.std_out = kwargs.get('std_out', '/dev/null')
        self.std_err = kwargs.get('std_err', '/dev/null')
        self.pid_file = kwargs.get('pid_file', '/dev/null')

    def __demonize__(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except (OSError,) as e:
            sys.stderr.write("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
            sys.exit(1)
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except (OSError,) as e:
            sys.stderr.write("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.std_in, 'r')
        so = open(self.std_out, 'a+')
        se = open(self.std_err, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pid_file
        atexit.register(self.__del_pid__)
        pid = str(os.getpid())
        open(self.pid_file, 'w+').write("%s" % pid)

    def __del_pid__(self):
        os.remove(self.pid_file)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pid_file to see if the daemon already runs
        try:
            pf = open(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?"
            sys.stderr.write(message % self.pid_file)
            sys.exit(1)

        # Start the daemon
        self.__demonize__()
        self.__run__()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pid_file
        try:
            pf = open(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pid_file %s does not exist. Daemon not running?"
            sys.stderr.write(message % self.pid_file)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except (OSError,) as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                print(str(err))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def __run__(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        demonized by start() or restart().
        """
        pass


class GsDemon(Demon, GsSocketServer):
    def __init__(self, *args, **kwargs):
        Demon.__init__(self, *args, **kwargs)
        GsSocketServer.__init__(self, *args, **kwargs)

    def start(self):
        Demon.start(self)

    def stop(self):
        # close socket
        self.disconnect()
        Demon.stop(self)

    def __run__(self):
        self.create_connection()
        self.run()