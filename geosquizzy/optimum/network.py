"""
=============================
Machine learning optimisation
=============================

#Settings
    1.Interface factors
        # Batch (the size of first sample for examination), if not provided 1% of document will be examined
        # Loss  (the threshold of Loss which should not be exceeded)

#Factors
    1.Diversity Factor
        M   = Amount of all unique key sequences(models)
        Pm  = Amount of specific (m) occurrences until the present diversity factor calculation
        DP  = Largest specific Key population max(Pm List)

        C = (DP * 100) / sum(P[0...N])
        Diversity Factor = (C - (100-C)) / M

#Weights/Inputs
    1.Percentage Growth of Diversity Factor
        Difference between two last calculation of Diversity Factor

        Increase = N -> N <= 0
        Decrease = N -> N >= 0

    2.The Strength of measurement
        The Amount of checked Elements as Percentage of total elements approximation

        (Checked_Elements * 100) / Total_Elements_Approximation

    3.Percentage Growth of All previous Diversity Factor calculations

#Aim
    *.Each machine learning process has to have some purpose|aim|target or the golden ratio to which
    it tend.
    *.Geo-squizzy target is to extract as many as possible unique structures/data_models of document with as few as
      possible items which will have to be traversed in order to obtain these unique keys.
    *.Beside of intended target, it will be probably very rare or even not possible to achieve some golden ratio. That is
      cause by: unknown structure of document, and very high probability of not linear location of data models.
    1.Considering all what was said above, the real AIM of geo-squizzy will be to achieve the best possible
      ratio (where ratio will be considered as relations between Loss(not traversed potential items which could result with
      new unique models have not seen already) and Diversity Factor)

    Summary.The main AIM then will be to achieve the largest speed of exploration
            with smallest possible ratio(Loss and Diversity Factor).

#Loss
    In order to gain speed, we always loss some precision(possible unique omitted data)
#

"""
from geosquizzy.optimum.utils import (diversity_factor, growth_of_diversity, strength_of_measurement)


class SeqModel:
    """
    Each SeqModel Class represent unique model structure
    extracted from traversing of JSON doc
    """

    def __init__(self, *args, **kwargs):
        self.keys = set(kwargs['keys'])
        self.count = 1

    def is_equal(self, new_keys):
        """
        :param new_keys:set([str,str...])
        :return:bool
        """
        if len(self.keys.symmetric_difference(new_keys)) == 0:
            self.count += 1
            return True
        else:
            return False


class RawData:

    def __init__(self, *args, **kwargs):
        self.models = []
        self.temp = set()

    def is_unique(self):
        """
        When traversing an object is completed we check for its presence
        If so it's count is increased else new SeqModel() is added
        :return None:
        """
        for x in self.models:
            if x.is_equal(self.temp):
                self.temp.clear()
                break
        if len(self.temp) != 0:
            self.models.append(SeqModel(keys=self.temp))
            self.temp.clear()

    def all_counts(self):
        return sum([x.count for x in self.models])

    def largest_seq(self):
        return max([x.count for x in self.models])


class Network:

    def __init__(self, *args, **kwargs):
        """
        kwargs['batch'] init() amount of initial batch sample on which first optimization will be done
        kwargs['loss'] float() possible loss as threshold
        """
        self.neurons = []
        self.__build_network__()

    def __build_network__(self):
        pass


class Optimum:

    def __init__(self, *args, **kwargs):
        """
        self.history is a 3 Dimensional Matrix [[int, int, int]...]
        """
        self.history = []
        self.Network = Network()
        self.RawData = RawData()

    def create_history(self, current, total):
        """
        Each invocation of this method will add new record to
        self.history
        :return:
        """
        x = diversity_factor(len(self.RawData.models), self.RawData.all_counts(), self.RawData.largest_seq())
        try:
            y = growth_of_diversity(self.history[-1], self.history[-2])
        except IndexError:
            y = growth_of_diversity(self.history[-1], self.history[-1])
        z = strength_of_measurement(current, total)
        self.history.append([x, y, z])


if __name__ == "__main__":
    pass