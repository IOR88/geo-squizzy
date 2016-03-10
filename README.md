# geo-squizzy

#### General  
0. last version geo-squizzy-0.1.2(stable)
1. no external dependencies

### Installation  
1.pip install geo-squizzy

#### Demo  
**See the <a href="http://geo.geschenk.ior88.megiteam.pl/">DEMO</a> page.**

### Usage
===================

Import
```python
from geosquizzy.geosquizzy import GeoSquizzy
```

Initialization(Currently support only for GeoJSON docs type FeatureCollection)
```python
geo_squizzy = GeoSquizzy()
```

Fetch data(keep in mind that data passed to start() method has to be in utf-8 format) 
and execute start() method
```python
data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/
                  master/build_big_data/test_data/ExampleDataPoint.json")
geo_squizzy.start(geojson=data)
```

Consume
```python
geo_squizzy.get_results()
```

### Documentation
===================
#### GeoSquizzy Methods

**GeoSquizzy.start(geojson=str(), is_doc=bool())**  
@geojson which has to be python str object which in it's structure
will reflect the GeoJSON structure.  

@is_doc python bool, default is None, setting this flag to True will prevent geo-squizzy from checking
if provided doc is a valid doc (validity here is very poor, checking only base structure of doc) and speed up
whole squizzy process  

**GeoSquizzy.get_results()**  
@return python list() object which consist of dict() elements where each has this structure  
{'values': ['-168.8205037850924', ' 131.69420530060995'], 'keys': ['coordinates', 'geometry', 'features']}  
@values example values of @keys[0]  
@keys a list of founded keys, presented in descending order(leaf -> root)  
