# geo-squizzy

### Implementations
0. https://github.com/LowerSilesians/geo-geschenk

### General

0. last version geo-squizzy-0.1.1(stable)
1. no external dependencies
3. tested successfully with python3.3 version

### Installation

1.pip install geo-squizzy

### Usage

```python

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import urlopen

from geosquizzy.squizzy import GeoSquizzy

"""
Example way to get data, important to decode it on utf-8 format
"""


def get_geojson(url=None):
    """
    get url data and decode it
    """
    res = urlopen(url=url)
    return res.read().decode('utf-8')


geo_squizzy = GeoSquizzy(geojson_doc_type="FeatureCollection")


"""
Geojson data has to be a valid geojson document type="FeatureCollection"
"""

data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/ExampleDataPoint.json")
geo_squizzy.geo_structure.start(geojson=data, is_doc=True)


"""
To get all keys
"""
for x in geo_squizzy.geo_structure.tree.get_all_leafs_paths():
    print(x, '\n')

```



