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


def protector(key, error):
    """
    @decorator function
    :param key: should be an instance boolean variable on which check is done
                if fn() can be executed
    """
    def wrap(f):
        def wrapped_f(*args):
            if getattr(args[0], key) is False:
                f(*args)
            else:
                raise error('This key and value are protected')
            f(*args)
        return wrapped_f
    return wrap