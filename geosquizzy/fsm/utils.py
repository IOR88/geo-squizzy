def create_unique_id(words, key):
    """
    Creating unique ids which represent keys in structure nodes,
    allowing us to store the same key names but which exist
    on different levels of doc structure
    """
    if key == 0:
        'parent'
        try:
            name = words[-2]
            return name + str(words.__len__() - 1)
        except IndexError:
            return None
    elif key == 1:
        'children'
        return words[-1] + str(words.__len__())


class WatchClass:
    """
    Watch will be triggered by setitem assignment x['attr'] = new
    if so happens then watch.check will be invoked
    """

    def __init__(self, *args, **kwargs):
        self.watch = kwargs['watch']
        self.value = kwargs['value']
        self.old_value = None

    def __setitem__(self, key, value):
        self.old_value = self.value
        self.value = value
        self.watch.check(old_value=self.old_value, new_value=self.value)
