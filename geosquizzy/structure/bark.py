
class TreeBark:
    """
    Main Responsibility of TreeBark class will be to keep information about
    already added structures({json object}, [array] etc...)

    For now we check only features items, so all keys above 1 level
    """
    def __init__(self, *args, **kwargs):
        self.repeated = False
        self.active = False
        self._id = 0
        self.keys = {}
        self.active_set = set()

    def add(self, leaf=None):
        if leaf['level'] > 1:
                self.active_set.add(leaf['id'])

    def __clean__(self):
        """
        execution of clean method means that one object was closed
        and next is going to be opened
        """
        self.active_set.clear()

    def new_object(self):
        """
        new_object() is invoked when DataAnatomyFiniteStateMachine in
        GeojsonFiniteStateMachine run() will observe closing of object
        """
        self.active = True
        if self.keys:
            self.__check_sets__()
        else:
            self.__add_set__()
            self.__clean__()

    def __check_sets__(self):
        """
        check all available sets and looking after difference, if active_set contain
        some key which is not present in other sets

        :return: as return it will manipulate self.repeated value
        """
        if len(self.active_set) > 0:
            for key, value in self.keys.items():
                if value.difference(self.active_set):
                    self.repeated = False
                else:
                    self.repeated = True

        if not self.repeated:
            self.__add_set__()
        self.__clean__()

    def __add_set__(self):
        """
        create new key and increase id number
        :return:
        """
        self.keys[str(self._id)] = self.active_set.copy()
        self._id += 1