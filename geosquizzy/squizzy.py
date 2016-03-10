from geosquizzy.structure import GeoJSON


class GeoSquizzy:

    def __init__(self, *args, **kwargs):
        self.geo_structure = GeoJSON(
            geojson_doc_type=kwargs['geojson_doc_type'])
