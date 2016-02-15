class GeoJSON:
    def __init__(self, *args, **kwargs):
        self.type = kwargs['geojson_doc_type']
        self.data = dict({"type": self.type, "features": []})
        pass

    def __read_geojson__(self):
        pass