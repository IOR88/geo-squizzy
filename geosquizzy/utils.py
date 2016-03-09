import re


def is_float(arg):
    return isinstance(arg, float)


def is_geojson_doc(arg):
    pattern = r'features'
    return bool(re.match(pattern, arg))


def get_string_slice(patterns, arg):
    """
    :param patterns: [regex,...]
    :param arg:  string
    :return: wanted string slice
    """
    while True:
        try:
            pattern = patterns.pop()
            parts = re.split(pattern, arg, maxsplit=1)
            arg = (parts[0].__len__() > parts[
                   1].__len__()) and parts[0] or parts[1]
        except IndexError:
            break
    return arg


# TODO some util to remove white spaces around value
# TODO could be use after traversing doc as cleaning function or sth
