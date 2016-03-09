from geosquizzy.structure import GeoJSON
from tests.getdata import get_geojson


class GeoSquizzy:

    def __init__(self, *args, **kwargs):
        self.geo_structure = GeoJSON(
            geojson_doc_type=kwargs['geojson_doc_type'])

# if __name__ == "__main__":
#     geo = GeoJSON(geojson_doc_type="FeatureCollection")
#     """
#     artificially generated geojson data
#     """
#     data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/dump1000.json")
#     """
#     live geojson data
#     """
#     # data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/ExampleDataPoint.json")
#     geo.start(geojson=data, is_doc=True)
