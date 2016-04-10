try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import urlopen


def get_geojson(url=None, path=None):
    """
    get url data and decode it
    """
    if url is not None:
        res = urlopen(url=url)
        return res.read().decode('utf-8')
        # http://stackoverflow.com/questions/30627937/tracebaclk-attributeerroraddinfourl-instance-has-no-attribute-exit
    else:
        file = open(path, 'r')
        data = file.read()
        file.close()
        return data

