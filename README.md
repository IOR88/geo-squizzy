# geo-squizzy

### General

1. support only for GeoJSON type "FeatureCollection"
2. no external dependencies
3. tested successfully with python3.3 version

### Installation

1.pip install geo-squizzy

### Usage

```python
from geosquizzy.squizzy import GeoSquizzy
from urllib import request

"""
Example way to get data, important to decode it on utf-8 format
"""


def get_geojson(url=None):
    """
    get url data and decode it
    """
    res = request.urlopen(url=url)
    with res as f:
        while True:
            return f.read().decode('utf-8')


geo_squizzy = GeoSquizzy(geojson_doc_type="FeatureCollection")


"""
Geojson data has to be a valid geojson document type="FeatureCollection"
"""

data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/ExampleDataPoint.json")
geo_squizzy.geo_structure.start(geojson=data, is_doc=True)


"""
To get all keys, a results will contain an [[str,str...],[]...]
                                           [[key,parent,parent,root]]
"""
geo_squizzy.geo_structure.tree.get_all_leafs_paths()


```



