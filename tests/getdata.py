try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import urlopen


def get_geojson(url=None):
    """
    get url data and decode it
    """
    res = urlopen(url=url)
    with res as f:
        while True:
            return f.read().decode('utf-8')

