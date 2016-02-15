from urllib import request

#TODO

def get_geojson(url=None):
    with request.urlopen(url=url) as f:
        while True:
            try:
                print(dir(f))
                s = f.read().decode('utf-8')
                #print(s)
                break
                print(s)
            except Exception:
                break

