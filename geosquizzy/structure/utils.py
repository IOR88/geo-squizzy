import re


def is_geojson_doc(arg):
    pattern = r'features'
    return bool(re.match(pattern, arg))