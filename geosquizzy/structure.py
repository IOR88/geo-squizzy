from copy import deepcopy
import geosquizzy.utils as utils
import geosquizzy.tokenizer as tokenizer
import geosquizzy.fsm as fsm


class Tree:

    def __init__(self, *args, **kwargs):
        self.leaf = dict({'id': None, 'name': None, 'children': [], 'level': 0,
                          'parent': None, 'completed': False, 'values': []})
        """
        @self.leaf completed property will announce that the leaf is ready
        """
        self.tree = dict()
        self.nodes = dict()

    def add_leaf(self, leaf=None):
        if leaf['parent'] is None:
            """root"""
            self.nodes[leaf['id']] = leaf
        elif self.nodes.get(leaf['id'], None) is None:
            """new leaf"""
            self.nodes[leaf['id']] = leaf

            if leaf['id'] not in self.nodes[leaf['parent']]['children']:
                """new children"""
                self.nodes[leaf['parent']]['children'].append(leaf['id'])

    def add_leaf_values(self, id=None, values=None):
        self.nodes[id]['values'] = values

    def get_all_leafs_paths(self):
        """we search through all nodes dict structure and for each element
           which have an empty children array we will start to construct search path,
           @query elements
            in order to store more then one key of the same name but which occurred on different nestedness level
            we have to provide unique name for it which is an @id, and for real key search representation we use
            @name attribute
            @id has to be used as well as linking key to describe inheritance
            child @id @name parent=@id | parent @id(child parent)
        """
        paths = []
        for x in self.nodes:
            new_key = {'keys': [], 'values': []}
            if self.nodes[x]['children'].__len__() == 0:
                # print(self.nodes[x]['name'], self.nodes[x]['values'], '\n')
                new_key['keys'].append(self.nodes[x]['name'])
                new_key['values'] = self.nodes[x]['values']
                last_parent = self.nodes[x]['parent']
                # if last parent is None at very begining it mean that it is very low level prop but if doesn't have children
                # then it has to be added as well
                if last_parent is None:
                    paths.append(new_key)
                while not (last_parent is None):
                    new_key['keys'].append(self.nodes[last_parent]['name'])
                    if not (self.nodes[last_parent]['parent'] is None):
                        last_parent = self.nodes[last_parent]['parent']
                    else:
                        paths.append(new_key)
                        last_parent = None
        return paths

    def prepare_new_leaf(self, **kwargs):
        new_leaf = deepcopy(self.leaf)
        new_leaf['id'] = kwargs.get('id', None)
        new_leaf['name'] = kwargs.get('name', None)
        new_leaf['level'] = kwargs.get('level', None)
        new_leaf['parent'] = kwargs.get('parent', None)
        return new_leaf


class FeaturesTree(Tree):

    def __init__(self, *args, **kwargs):
        # super(FeaturesTree, self).__init__(*args, **kwargs)
        Tree.__init__(self, *args, **kwargs)


class GeoJSON:

    def __init__(self, *args, **kwargs):
        self.type = kwargs['geojson_doc_type']
        self.data = dict({"type": self.type, "features": []})
        self.tree = FeaturesTree()
        self.tokenizer = tokenizer.JsonTokenizer(structure=self.tree)
        self.fsm = fsm.GeojsonFiniteStateMachine(structure=self.tree)
        self.geojson = None
        self.percentage = None
        self.is_doc = False

    def start(self, **kwargs):
        """
        kwargs['is_doc'] is optional flag but provided will grow
        the performance, we will not have to check if doc is a chunk or full doc
        """
        self.geojson = kwargs.get('geojson', None)
        self.percentage = kwargs.get('percentage', None)
        self.is_doc = kwargs.get('is_doc', False)
        self.__read_geojson__()

    def get_results(self):
        return self.tree.get_all_leafs_paths()

    def __read_geojson__(self):
        """
        @self.percentage How much of the provided geojson should be checked, default is set to all
        @self.geojson String which can represent both or full geojson document or what will be in favour for future
         improvements it could be a chunk of String which consist a full geojson document

        as main activity it should all the time update self.tree nodes
        """

        if self.is_doc or utils.is_geojson_doc(self.geojson):
            """
            geojson doc mode
            when we are getting a full geojson object we need only to get a features array
            to achieve it we use to regex patterns, which are very general and should give us the [features inside]
            """
            # patterns = [r'(?:[,\s]*)"features":(?:[\s]*)',
            #             r'(?:[,\s]*)"type":(?:[\s]*)"FeatureCollection"(?:[,\s]*)']
            # features_string = utils.get_string_slice(patterns, self.geojson)
            self.fsm.run(data=self.geojson)
        else:
            """
            geojson chunk mode
            """
            pass
