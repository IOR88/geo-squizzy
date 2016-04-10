class GeoSquizzyResults:

    def __init__(self, *args, **kwargs):
        self.results = []
        self.options = kwargs.get('outcome_options', {})

    def get_results(self, nodes=None):

        for x in nodes:
            new_key = {'keys': [], 'values': []}

            if nodes[x]['children'].__len__() == 0:

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

        return self.results

    # TODO
    def get_partial_results(self):
        pass