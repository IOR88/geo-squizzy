def pre_data_bytes_stream(data, **kwargs):
    # d = bytes(', '.join("{!s}={!r}".format(k, v) for (k, v) in data.items()), 'utf-8')
    return bytes(str(data), 'utf-8')