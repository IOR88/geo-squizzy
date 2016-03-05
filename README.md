# geo-squizzy

### General

0. last version geo-squizzy-0.1.dev3(stable)
1. no external dependencies
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

data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/dump1000.json")
geo_squizzy.geo_structure.start(geojson=data, is_doc=True)


"""
To get all keys, a results will contain an [{}...] where {'values': ['Point'], 'keys': ['type', 'geometry', 'features']}
@values potential value that can be search for
@keys a way from the leaf(left) to root(right)
"""
geo_squizzy.geo_structure.tree.get_all_leafs_paths()


```



