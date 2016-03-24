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
        :param kwargs['id']: int(01) where first is a layer
        and second is an number id within layer, id is unique for whole network
        """
        self.id = kwargs['id']
        self.importance = kwargs['importance']
        self.weight = 0
        self.synapses = []

    def add_synapse(self, neuron_id):
        self.synapses.append(neuron_id)

    def adjust_weight(self):
        pass