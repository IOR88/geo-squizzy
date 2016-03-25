"""
EconomizeFiniteStateMachine together with DataAnatomyFiniteStateMachine TreeBark Classes
is turning on and turning off main run()

Right now criteria is very simple, unique key sequence for feature object always bringing intersections
intervals to 0(all-objects-are-check-one-by-one) and each repeatable sequence is increasing intersections interval by 1
so(OBJECT_TRAVERSING...WAITING_TIME(INTERSECTIONS INTERVAL)...OBJECT_TRAVERSING  ETC...)
"""


class EconomizeFiniteStateMachine:
    def __init__(self, *args, **kwargs):
        """
        self.omitted_obj keep information about all omitted_obj for active batch
        """
        self.space = 0
        self.traversed = 0
        self.omitted_obj = 0

    def adjust_space(self, exist):
        if exist:
            self.space += 1
        else:
            self.space = 0
        # print(self.space)
        self.omitted_obj = 0

    def increase_progress(self):
        self.traversed += 1
        if self.traversed >= self.space:
            self.traversed = 0

    def omit(self):
        self.omitted_obj += 1
        # print(self.omitted_obj)

    def economize(self):
        return self.traversed is not 0