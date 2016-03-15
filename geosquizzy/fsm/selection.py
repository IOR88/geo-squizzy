# TODO selection percentage pattern works, but run and done methods really slow down
# TODO whole computation when we traverse really big data

# TODO in order to achieve better performance EconomizeFiniteStateMachine class was provided

import math


class SelectionFiniteStateMachine:
    def __init__(self, *args, **kwargs):
        self.empty_passage = False
        self.obj_temp_size = 0
        self.obj_size = 0
        self.visited = -1
        self.visited_total = -1
        self.to_visit = 0
        self.space = 0
        self.intersections = -1
        self.items = 0
        self.doc_len = kwargs.get('len', 0)
        self.percentage = kwargs.get('percentage', 0)
        self.immersion = {'features': [0, 1],
                          'features_obj': [0, 1, 0]}

    def run(self, anatomy=None, blocked=None):
        """
        when data stream will nest itself in features array, we start to checking
        if data stream is inside of features item or outside before entering next item

        :param anatomy: DataAnatomyFiniteStateMachine.stack [int,...]
        :return: bool()
        """
        if self.immersion['features'] == anatomy and not self.empty_passage:
            self.visited_total += 1
            self.intersections += 1
            self.empty_passage = True

            if blocked:
                self.obj_temp_size = 0
            else:
                self.visited += 1
                self.__adjust_information__()

            if self.intersections >= self.space:
                self.intersections = 0
        elif self.immersion['features_obj'] == anatomy[:3]:
            self.empty_passage = False
            self.obj_temp_size += 1
        return self.intersections >= 1

    def done(self):
        return self.visited >= self.to_visit and self.to_visit != 0

    def __adjust_information__(self):
        if self.obj_temp_size > self.obj_size:
            self.obj_size = self.obj_temp_size
            self.__calculate_percentage__()
            self.__calculate_space__()
        self.obj_temp_size = 0

    def __calculate_percentage__(self):
        self.items = math.floor(self.doc_len / self.obj_size)
        to_visit = math.floor(((self.items * self.percentage) / 100) - self.visited)
        self.to_visit = (1, to_visit)[to_visit >= 0]

    def __calculate_space__(self):
        self.space = math.floor(self.items / (self.to_visit + self.visited))