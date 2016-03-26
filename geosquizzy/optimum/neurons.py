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
        return self.sense(x) + self.weight, self.sense.__name__

    def back_propagate(self):
        pass


def strength(x):
    """
    :param x [x, y, z, k, g] history record

    scala 0 - 100

    Neuron sense, strength can have positive or negative weight for optimization of whole algorithm
    It will be based on x[0] percentage of the biggest population and on level of x[1](not matter if
    is a -INT or +INT, what's count is the size of number)
    """
    return (((x[0]+abs(x[1]))*100)/100)/10


def worry(x):
    """
    :param x [x, y, z, k, g] history record

    Neuron sense, worry will focus on relation between
    x[2] and x[5] where first is a batch size and second the
    percentage of omitted objects according to total objects
    """

    y = (x[2] - x[5])
    if y == x[2]:
        return 0
    else:
        return y/10


def rationality(x):
    """
    :param x [x, y, z, k, g] history record

    Neuron sense, rationality will focus on x[4] which is a
    difference in omitted objects between current and last history record
    """
    # print(x)
    try:
        return x[3]/x[4]
    except ZeroDivisionError:
        return 0