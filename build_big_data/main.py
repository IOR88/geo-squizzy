import random
import json
from models import CITY


class Duplicates:
    def __init__(self):
        self.storage = dict()
        pass


class Feature:
    def __init__(self, *args, **kwargs):
        self.data = dict({"type": "Feature", "properties": dict(), "geometry": {"type": kwargs['type'], "coordinates": []}})
        self.data['properties'] = kwargs['model']().get_random_data()

    def add_coordinates(self, coordinates=None):
        self.data['geometry']['coordinates'] = coordinates


class DataStructure:
    def __init__(self, *args, **kwargs):
        self.data = dict({'type': kwargs['type'], 'features': []})
        self.duplicates = Duplicates()
        self._range = kwargs['coordinates_range']
        self.feature_model = kwargs['feature_model']
        self.feature_type = kwargs['feature_type']
        self.__run__(number=kwargs['features_number'])
        pass

    def __run__(self, number=None):
        self.data['features'] = [self.feature() for x in range(0, number, 1)]
        pass

    def coordinates(self):
        x = random.uniform(self._range[0], self._range[1])
        case = self.duplicates.storage.get(x, None)
        while case is not None:
           x = random.uniform(self._range[0], self._range[1])
           case = self.duplicates.storage.get(x, None)

        self.duplicates.storage[x] = x
        return x

    def feature(self):
        feature = Feature(type=self.feature_type, model=self.feature_model)
        feature.add_coordinates(coordinates=[self.coordinates(), self.coordinates()])
        return feature.data


if __name__ == "__main__":
    geo = DataStructure(type="FeatureCollection",
                        feature_type="Point",
                        coordinates_range=[float(-200), float(200)],
                        features_number=500000,
                        feature_model=CITY)
    geo_json = json.dumps(geo.data)
    f = open("data/dump500000.json", "w")
    f.write(geo_json)
    f.close()