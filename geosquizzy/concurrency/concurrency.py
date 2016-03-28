"""
==================
Concurrency Module
==================
"""
from multiprocessing import Process, Pipe
import time


class FlowStorage():
    """
    MotionDispatcher Class keep connection between all processes(relation is master(write), slave(read))
    """

    def __init__(self, *args, **kwargs):
        self.amount = -1
        self.pipes = {}

    def create_pip(self):
        """
        slave read, master write
        1-Read 2-Write Pipe(False)
        1-RW   2-RW    Pipe()
        :return:
        """
        slave, master = Pipe(False)
        self.amount += 1
        self.pipes[str(self.amount)] = {'master': master, 'slave': slave}
        return self.amount

    def get_pipe_end(self, key, role):
        """
        :param key:  str(int)
        :param role: master or slave
        :return: Pipe()
        """
        return self.pipes[str(key)][role]


class SquizzyProcess(Process):
    def __init__(self, *args, **kwargs):
        super(SquizzyProcess, self).__init__(*args, **kwargs)

    def run(self):
        print('run')
        pass


if __name__ == "__main__":
    a = SquizzyProcess(target=lambda x: print(x), args=(1,))
    print(a)
    a.start()
    pass