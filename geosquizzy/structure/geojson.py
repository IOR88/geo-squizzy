from exceptions.exceptions import *
from utils import *


class Feature:

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs: data -> appropriate data representation to create dict
        :return: Feature object

        Base Class which represent Feature object with basic data validation
        """
        try:
            self.data = dict(kwargs['data'])
        except Exception:
            """
            Exception will be raised if dict() initialization will fail
            """
            raise FeatureSyntaxError()

        geometry = self.data.get("geometry", None)
        properties = self.data.get("geometry", None)
        feature = self.data.get("type", None)
        if not geometry or not properties or feature is not "Feature":
            """
            Exception will be raised feature object is not an valid feature
            object according to geojson docs
            """
            raise FeatureStructureError()

    def validate(self):
        pass

    def is_feature_type(self):
        return self.data["type"] == self.name


class PointFeature(Feature):

    def __init__(self, *args, **kwargs):
        super(PointFeature, self).__init__(*args, **kwargs)
        self.name = "Point"

    def validate_point(self):
        for x in self.data["geometry"]["coordinates"]:
            if not is_float(x):
                raise FeatureCoordinatesError()
        if not self.is_feature_type():
            raise Exception("\nWrong type provided for PointFeature Class.")

    def validate(self):
        super(PointFeature, self).validate()
        self.validate_point()


class MultiPointFeature(Feature):

    def validate(self):
        pass


class LineStringFeature(Feature):

    def validate(self):
        pass


class MultiLineStringFeature(Feature):

    def validate(self):
        pass


class PolygonFeature(Feature):

    def validate(self):
        pass


class MultiPolygonFeature(Feature):

    def validate(self):
        pass


if __name__ == "__main__":
    data_ok = {"geometry": {"type": "Poin",
                            "coordinates": [-122.93770201248995,
                                            146.32791746493376]},
               "properties": {"code": 4402,
                              "name": "BZgtQyEu",
                              "citizens": 351641,
                              "country": "WKyCMBr"},
               "type": "Feature"}

    test = PointFeature(data=data_ok)
    test.validate()