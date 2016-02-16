from urllib import request


def get_geojson(url=None):
    """
    get url data and decode it
    """
    res = request.urlopen(url=url)
    with res as f:
        while True:
            return f.read().decode('utf-8')

