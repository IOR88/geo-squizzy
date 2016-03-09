# geo-squizzy

### General

0. last version geo-squizzy-0.1.1(stable)
1. no external dependencies
3. tested successfully with python3.3 version

### Installation

1.pip install geo-squizzy

### Usage

Import
```python
from geosquizzy.squizzy import GeoSquizzy
```

Initialization(Currently support only for GeoJSON docs type FeatureCollection)
```python
geo_squizzy = GeoSquizzy(geojson_doc_type="FeatureCollection")
```

Fetch data(keep in mind that data passed to start() method has to be in utf-8 format) 
and execute start() method
```python
data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/
                  master/build_big_data/test_data/ExampleDataPoint.json")
geo_squizzy.start(geojson=data, is_doc=True)
```

Consume
```python
geo_squizzy.get_results()
```

### Documentation
