from geosquizzy.fsm.fsm import GeojsonFiniteStateMachine
from geosquizzy.structure.outcome import GeoSquizzyResults
from geosquizzy.optimum.network import Optimum
from geosquizzy.gs_socket.gs_client import GsSocketClient

from socket import AF_INET, SOCK_STREAM
import threading
import queue


class Tree:

    def __init__(self, *args, **kwargs):
        self.nodes = dict()


class FeaturesTree:

    def __init__(self, *args, **kwargs):
        self.Tree = Tree(*args, **kwargs)
        self.Res = GeoSquizzyResults(*args, **kwargs)
        self.Optimum = Optimum(*args, **kwargs)
        # self.socket = kwargs.get('socket', None)

    @staticmethod
    def __new__leaf__():
        leaf = dict({'id': None, 'name': None, 'children': [], 'level': None,
                     'parent': None, 'completed': False, 'values': []})
        return leaf

    def prepare_new_leaf(self, **kwargs):
        new_leaf = self.__new__leaf__()
        return {x: kwargs[x] if y is None else y for x, y in new_leaf.items()}

    def new_obj(self, omitted):
        self.Optimum.update_data(omitted)

    def add_leaf(self, leaf=None):
        """
        :param leaf new node/leaf dict():
        :return:boolean(which mean if node already exist)
        """
        self.Optimum.update_seq(leaf=leaf)

        # self.socket.write(self.get_all_leafs_paths(progress=True))
        # self.socket.run(leaf)

        if leaf['parent'] is None:
            self.Tree.nodes[leaf['id']] = leaf

        elif self.Tree.nodes.get(leaf['id'], None) is None:
            self.Tree.nodes[leaf['id']] = leaf

            if leaf['id'] not in self.Tree.nodes[leaf['parent']]['children']:
                self.Tree.nodes[leaf['parent']]['children'].append(leaf['id'])

        if self.Optimum.fit_optimum:
            self.Optimum.fit_optimum = False
            return self.Optimum.prediction

    def add_leaf_values(self, leaf_id=None, leaf_values=None):
        self.Tree.nodes[leaf_id]['values'] = leaf_values

    def get_all_leafs_paths(self, progress=None):
        return self.Res.get_results(nodes=self.Tree.nodes, progress=progress)


class GeoJSON:

    def __init__(self, **kwargs):
        self.Socket = GsSocketClient(**kwargs.get('socket_options'))
        self.ProgressQueue = queue.Queue()
        self.FeTree = FeaturesTree(**kwargs)
        self.Fsm = GeojsonFiniteStateMachine(progress_queue=self.ProgressQueue, structure=self.FeTree)

        self.geojson = None
        self.options = kwargs.get('geojson_options', {})

        self.__processes__()

    def __processes__(self):
        # self.Socket.connect()
        self.SocketThread = threading.Thread(target=self.Socket.run, args=(self.ProgressQueue, self.__get_results__))
        self.SocketThread.start()

    def __start__(self, **kwargs):
        self.geojson = kwargs.get('geojson', None)
        self.__read_geojson__(**kwargs)

    def __get_results__(self, progress=None):
        # [print(x.keys, x.count) for x in self.FeTree.Optimum.RawData.models]
        # [print(x) for x in self.FeTree.Optimum.history]
        return self.FeTree.get_all_leafs_paths(progress=progress)

    def __read_geojson__(self, **kwargs):
        if self.options['mode'] == 'static':
            self.Fsm.run(data=self.geojson, **kwargs)
        elif self.options['mode'] == 'dynamic':
            pass
