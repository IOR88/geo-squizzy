# geo-squizzy


#### General
0. last version geo-squizzy-0.2.2(stable)
1. last version geo-squizzy-0.2.2.dev0(unstable)
2. no external dependencies

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

geojson_options = {'mode': 'static', 'geojson_type': 'FeatureCollection'}
outcome_options = {}
optim = {'batch': 1, 'loss': -5.0}
socket_options = {'HOST': 'localhost',
                  'PORT': 8030,
                  'FAMILY': AF_INET,
                  'TYPE': SOCK_STREAM}

geojson_options = {'geojson_options': geojson_options},
                   'outcome_options': outcome_options,
                   'optim': optim,
                   'socket_options': socket_options}

geo_squizzy = GeoSquizzy(**geojson_options)
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

**GeoSquizzy(kwargs)**    
@geojson_options: **only possible and required option for now {'mode': 'static', 'geojson_type': 'FeatureCollection'}**  
@outcome_options: **no kwargs for this options**  
@optim: **required**   
    &nbsp;&nbsp;&nbsp;  **@batch** is the size of a item group on which optimization will be made range(1, +oo)  
    speed of algorithm grows with decrease of batch size   
    &nbsp;&nbsp;&nbsp;  **@loss** factor of possible data loss range(-oo, +oo)    
    speed of algorithm grows when loss head to minus infinity      
@socket_options: **no required**  
    &nbsp;&nbsp;&nbsp;  **If added, together with GsDemon allow for interactive communication with algorithm**    

**GeoSquizzy.get_results()**  
@return python list() object which consist of dict() elements where each has this structure  
{'values': ['-168.8205037850924', ' 131.69420530060995'], 'keys': ['coordinates', 'geometry', 'features']}  
@values example values of @keys[0]  
@keys a list of founded keys, presented in descending order(leaf -> root)

#### GsDemon methods

```python

from demon.gs_demon import GsDemon
  
from socket import AF_INET, SOCK_STREAM  

import sys  
```

GsDemon example run script

```python

if __name__ == "__main__":
```    

```python

demon = GsDemon(pid_file='PATH/logs/pid.txt',
                std_in='PATH/logs/in.txt',
                std_out='PATH/logs/out.txt',
                std_err='PATH/logs/err.txt',
                HOST='localhost',
                PORT=PORT,
                FAMILY=AF_INET,
                TYPE=SOCK_STREAM,
                CONNECTIONS=INT)
if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
        demon.start()
    elif 'stop' == sys.argv[1]:
        demon.stop()
    elif 'restart' == sys.argv[1]:
        demon.restart()
    else:
        print("Unknown command")
        sys.exit(2)
    sys.exit(0)
else:
    print("usage: %s start|stop|restart" % sys.argv[0])
    sys.exit(2)
    
```

```
python demon_script.py start || stop || restart
```

After initializing demon, we can provide socket_options for geosquizzy client  
which will communicate with demon(for now sending new keys), demon will then
broadcast all new messages to other clients  
  
**Example will be provided with geogeschenk demo app**  
**Server** [https://github.com/LowerSilesians/geo-geschenk-server](https://github.com/LowerSilesians/geo-geschenk-server)  
**Client**  
(If You would create a client socket and listen(read data) on demon port
then all the time during algorithm work You would be informed about new keys  
