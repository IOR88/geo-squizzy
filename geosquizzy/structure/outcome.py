class GeoSquizzyResults:

    def __init__(self, *args, **kwargs):
        self.progress_results = set()
        self.results = []
        self.options = kwargs.get('outcome_options', {})

    def get_results(self, nodes=None, progress=None):

        self.results = []

        for x in nodes:

            if nodes[x]['children'].__len__() == 0:

                if not (progress is None) and nodes[x]['name'] not in self.progress_results:
                    self.progress_results.add(nodes[x]['name'])
                    self.__get_parents__(nodes, x)
                elif progress is None:
                    self.__get_parents__(nodes, x)

        return self.results

    def __get_parents__(self, nodes, x):

            new_key = {'keys': [], 'values': []}
            new_key['keys'].append(nodes[x]['name'])
            new_key['values'] = nodes[x]['values']
            last_parent = nodes[x]['parent']

            if last_parent is None:
                self.results.append(new_key)

            while not (last_parent is None):
                new_key['keys'].append(nodes[last_parent]['name'])

                if not (nodes[last_parent]['parent'] is None):
                    last_parent = nodes[last_parent]['parent']
                else:
                    self.results.append(new_key)
                    last_parent = None