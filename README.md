# geo-squizzy

### General

0. last version geo-squizzy-0.1.1(stable)
1. no external dependencies
3. tested successfully with python3.3 version

### Installation

1.pip install geo-squizzy

### Usage

```python
from geosquizzy.squizzy import GeoSquizzy
```

"""
Example way to get data, important to decode it on utf-8 format decode('utf-8')
"""

```python
geo_squizzy = GeoSquizzy(geojson_doc_type="FeatureCollection")
```


Geojson data has to be a valid geojson document type="FeatureCollection"


```python
data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/ExampleDataPoint.json")
geo_squizzy.start(geojson=data, is_doc=True)
```


```python
geo_squizzy.get_results()
```



