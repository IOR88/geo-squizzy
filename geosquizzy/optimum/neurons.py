"""
=============================
Neurons
1.each neuron will have synapses['connections'] with other neurons
  (it could be presented as directed graph, where vectors connections go
   from input data to last neuron layer and finally to activation function)

2.each neuron will have its importance||strength of the impulse

3.each neuron will have its weight which will be mutable
=============================
"""


class Neuron:
    def __init__(self, *args, **kwargs):
        """
        :param kwargs['id']: tuple (int(),int()) where first is a layer
        and second is an number id within layer, id is unique for whole network
        """
        self.id = kwargs['_id']
        self.importance = kwargs.get('importance', 0)
        self.sense = kwargs.get('sense')
        self.weight = 0
        self.synapses = []

    def add_synapse(self, neuron_id):
        self.synapses.append(neuron_id)

    def adjust_weight(self, n_weight):
        self.weight = self.weight + n_weight

    def calculate_sig(self, x):
        return self.sense(x) + self.weight

    def back_propagate(self):
        pass


def strength(x):
    """
    Neuron sense, strength can have positive or negative weight for optimization of whole algorithm
    It will be based on x[0] percentage of the biggest population and on level of x[1](not matter if
    is a -INT or +INT, what's count is the size of number)
    """
    pass


def worry(x):
    """
    Neuron sense, worry will focus on relation between
    x[2] and x[3] where first is a batch size and second the
    number of omitted objects
    """
    pass


def rationality(x):
    """
    Neuron sense, rationality will focus on x[4] which is a
    difference in omitted objects between current and last history record
    """
    pass