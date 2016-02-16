import re


def is_float(arg):
    return isinstance(arg, float)


def is_geojson_doc(arg):
    pattern = r'features'
    return bool(re.match(pattern, arg))


def get_string_slice(pattern, string, maxsplit):
    """
    :param pattern: regex
    :param string:  string
    :param maxsplit: int
    :return: wanted string slice
    """
    parts = re.split(pattern, string, maxsplit=maxsplit)
    #print(parts)
    #return parts[1]