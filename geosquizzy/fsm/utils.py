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