"""

The highest abstraction layer of geosquizzy which hand over interfaces for users

"""

from geosquizzy.structure.structure import GeoJSON


class GeoSquizzy:

    def __init__(self, *args, **kwargs):
        self.Geo = GeoJSON(**kwargs)

    def start(self, **kwargs):
        self.Geo.__start__(**kwargs)

    def get_results(self):
        return self.Geo.__get_results__()