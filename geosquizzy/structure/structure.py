from geosquizzy.fsm.fsm import GeojsonFiniteStateMachine
from geosquizzy.structure.outcome import GeoSquizzyResults
from geosquizzy.structure.bark import TreeBark
from geosquizzy.optimum.network import Optimum



class Tree:

    def __init__(self, *args, **kwargs):
        self.nodes = dict()


class FeaturesTree:

    def __init__(self, *args, **kwargs):
        self.Tree = Tree(*args, **kwargs)
        self.Res = GeoSquizzyResults(*args, **kwargs)
        self.Optimum = Optimum(*args, **kwargs)

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

    def get_all_leafs_paths(self):
        return self.Res.get_results(nodes=self.Tree.nodes)


class GeoJSON:

    def __init__(self, **kwargs):
        self.FeTree = FeaturesTree(**kwargs)
        self.Fsm = GeojsonFiniteStateMachine(structure=self.FeTree)
        self.geojson = None
        self.options = kwargs.get('geojson_options', {})

    def __start__(self, **kwargs):
        self.geojson = kwargs.get('geojson', None)
        self.__read_geojson__(**kwargs)

    def __get_results__(self):
        # [print(x.keys, x.count) for x in self.FeTree.Optimum.RawData.models]
        # [print(x) for x in self.FeTree.Optimum.history]
        return self.FeTree.get_all_leafs_paths()

    def __read_geojson__(self, **kwargs):
        if self.options['mode'] == 'static':
            self.Fsm.run(data=self.geojson, **kwargs)
        elif self.options['mode'] == 'dynamic':
            pass
