import math
# TODO should be configure to save doc structure in fly and depending on that counting percentage
# TODO right know is only adjusted for GeoJSON FeatureCollection


class SelectionFiniteStateMachine:
    def __init__(self, *args, **kwargs):
        self.obj_temp_size = 0
        self.obj_size = 0
        self.visited = -1
        self.to_visit = 0
        self.space = 0
        self.intersection = -1
        self.items = 0
        self.doc_len = kwargs.get('len', 0)
        self.percentage = kwargs.get('percentage', 0)
        self.immersion = {'features': [0, 1],
                          'features_obj': [0, 1, 0]}

    def run(self, anatomy=None):
        """
        when data stream will nest itself in features array, we start to checking
        if data stream is inside of features item or outside before entering next item

        :param anatomy: DataAnatomyFiniteStateMachine.stack [int,...]
        :return: bool()
        """
        condition = self.immersion['features'] == anatomy
        if condition:
            self.__adjust_information__()
            self.obj_temp_size = 0
            self.visited += 1  # TODO we starting from -1 so values is reliable
            self.intersection += 1
            if self.intersection >= self.space:
                self.intersection = 0
        else:
            self.obj_temp_size += 1

        return self.intersection > 1  # TODO changing blocked flag

    def done(self):
        return self.visited >= self.to_visit and self.to_visit != 0

    def __adjust_information__(self):
        if self.obj_temp_size > self.obj_size:
            self.obj_size = self.obj_temp_size
            self.__calculate_percentage__()
            self.__calculate_space__()

    def __calculate_percentage__(self):
        # TODO not a best idea to adjust it all the time should be compare with all previous differences
        self.items = self.doc_len / self.obj_size
        self.to_visit = math.floor(((self.percentage * self.items) / 100) - self.visited)

    def __calculate_space__(self):
        print(self.items, self.to_visit)
        self.space = math.floor(self.items / self.to_visit)
        print(self.space)