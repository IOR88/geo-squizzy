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
from geosquizzy.optimum.utils import (diversity_factor, growth_of_diversity, strength_of_measurement, loss, activation)
from geosquizzy.optimum.neurons import (Neuron, strength, worry, rationality)


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

    def update_seq(self, leaf):
        self.temp.add(leaf['id'])

    def all_counts(self):
        return sum([x.count for x in self.models])

    def largest_seq(self):
        return max([x.count for x in self.models])


class Network:

    def __init__(self, *args, **kwargs):
        """
        kwargs['layers'] int() number of neuron layers
        kwargs['neurons'] int() number of neurons per layer
        """
        self.neurons = {}
        self.i_layers = kwargs['layers']
        self.i_neurons = kwargs['neurons']
        self.i_senses = kwargs['senses']
        self.build_network()

    def build_network(self):
        [self.__add_layer__(self.i_neurons, x, self.i_senses[x]) for x in range(0, self.i_layers, 1)]
        self.__create_synapses__()

    def __add_layer__(self, neurons, layer, senses):
        [self.__add_neuron__((layer, x), senses[x]) for x in range(0, neurons, 1)]

    def __add_neuron__(self, n_id, sense):
        hash_k = str(n_id[0])+str(n_id[1])
        self.neurons[hash_k] = Neuron(_id=n_id, sense=sense)

    def __create_synapses__(self):
        [self.__connect_layers__(x) for x in range(0, self.i_layers, 1)]

    def __get_neurons__(self, x_layer):
        """
        :param x_layer: neurons layer
        get all neurons which belong to x_layer
        """
        return [x for x in self.neurons.keys() if x[0] == str(x_layer)]

    def __connect_layers__(self, x_layer):
        """
        :param x_layer is a layer for which connections will be created
        get all neurons which are between x_layer -1 and +1, then for
        each neuron which belong to x_layer we create synapse connection for all
        neurons from to_connect LIST
        """
        to_connect = []
        if x_layer - 1 >= 0:
            to_connect = self.__get_neurons__(x_layer-1)
        if x_layer + 1 < self.i_layers:
            to_connect += self.__get_neurons__(x_layer+1)

        [self.neurons[x].add_synapse(y) for x in self.__get_neurons__(x_layer) for y in to_connect]

    def interpret_signal(self, data, max_loss):
        """
        :param data: [x, y, z, k, g] one last record from history
        trigger data flow into neurons network
        """
        # print(data)
        information_package = [x[1].calculate_sig(data) for x in self.neurons.items()]
        # print(information_package)
        prediction = activation(information_package, max_loss)

        _loss = loss(information_package, data)
        if _loss > max_loss:
            """
            TODO adjust signals
            """
            pass

        return prediction


class Optimum:

    def __init__(self, *args, **kwargs):
        """
        :param kwargs['optim'] batch and loos params
        self.history is a 3 Dimensional Matrix [[int, int, int]...]
        """
        self.batch = kwargs.get('optim', None).get('batch', 100)
        self.loss = kwargs.get('optim', None).get('loss', 1.0)
        self.last_batch = 0
        self.fit_optimum = False
        self.prediction = None
        self.history = []
        self.Network = Network(layers=1, neurons=3, senses=[[strength, worry, rationality]])
        self.RawData = RawData()

    def __create_history__(self, current, total, omitted):
        """
        Each invocation of this method will add new record to
        self.history
        :return:
        """
        x = diversity_factor(len(self.RawData.models), self.RawData.all_counts(), self.RawData.largest_seq())
        try:
            y = growth_of_diversity(x, self.history[-1][0])
            g = omitted - self.history[-1][3]
        except IndexError:
            # y = growth_of_diversity(self.history[-1], self.history[-1])
            y = 0
            g = 0
        z = strength_of_measurement(current, total)
        k = omitted
        f = (omitted*100)/total
        self.history.append([x, y, z, k, g, f])

    def update_data(self, omitted):
        self.RawData.is_unique()
        self.__fit_needed__(omitted)

    def update_seq(self, leaf):
        self.RawData.update_seq(leaf)

    def __fit_needed__(self, omitted):
        t_count = self.RawData.all_counts()
        # print(t_count)
        if (t_count - self.last_batch) >= self.batch:
            self.__create_history__(self.batch, 10000, omitted)
            self.prediction = self.Network.interpret_signal(self.history[-1], self.loss)
            # print(self.prediction)
            self.last_batch = t_count
            self.fit_optimum = True