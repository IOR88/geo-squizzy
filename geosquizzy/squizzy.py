from geosquizzy.structure import GeoJSON
from tests.getdata import get_geojson

#TODO lib itself will not make any requests but it
#TODO should have some kind of buffer reader, so as result it will get response object or promise ?

#TODO other way arround would be to have this buffer reader by lib whihc mean that lib will explicitly take only objects when
#TODO when they are buffered enough to create json item, the chunks TODO will be sent by some API deamon to both lib as
#TODO key searcher and maybe already to mongoDB which will be used then for filtering(when we have keys)



#TODO TWO multiprocesses ? each would have two threads maybe, thanks to that we would check different parts of recived data
#TODO but that should be done by Lib Deamon API not by Lib itself


class GeoSquizzy:
    def __init__(self):
        pass

if __name__ == "__main__":
    geo = GeoJSON(geojson_doc_type="FeatureCollection")
    data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/dump1000.json")
    print(data)