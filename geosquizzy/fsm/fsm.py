from geosquizzy.fsm.utils import (create_unique_id, WatchClass)
from geosquizzy.fsm.data import (DataPortFiniteStateMachine, DataAnatomyFiniteStateMachine)
from geosquizzy.fsm.commands import CommandsFiniteStateMachine
from geosquizzy.fsm.states import (StatesCollector, InterpretState, WriteState, SaveState, RemoveState)


class MBC(WatchClass):
    def __init__(self, *args, **kwargs):
        super(MBC, self).__init__(*args, **kwargs)


class GeojsonFiniteStateMachine:

    def __init__(self, *args, **kwargs):
        """
        :param kwargs['structure']: FeaturesTree Class
        """
        self.DataPort = DataPortFiniteStateMachine(structure=kwargs['structure'])
        self.DataAnatomy = DataAnatomyFiniteStateMachine()
        self.Com = CommandsFiniteStateMachine()

        self.StatesCollector = StatesCollector()
        self.InterpretState = InterpretState(collector=self.StatesCollector),
        self.WriteState = WriteState(collector=self.StatesCollector),
        self.SaveState = SaveState(collector=self.StatesCollector),
        self.RemoveState = RemoveState(collector=self.StatesCollector),

        self.MBC = MBC(value=[1, 0, 0, 0], watch=self.StatesCollector)
        self.command = self.initial_state()

    def initial_state(self):
        return self.Com.get_command(char='0', mbc='0')

    def run(self, **kwargs):
        """
        @kwargs['data'] features array
        @self.MBC[0] is set to 1 to run Interpret state as initial one
        """
        self.DataPort.data = kwargs['data']

        for i, k in enumerate(self.DataPort.data):

            self.DataAnatomy.update_structure(char=k)

            if self.MBC.value[0] == 1:

                self.InterpretState = InterpretState()
                self.InterpretState.run(FSM=self, char=k)

            if self.MBC.value[1] == 1:

                self.WriteState = WriteState()
                self.WriteState.run(FSM=self, char=k)

            if self.MBC.value[2] == 1:

                self.SaveState = SaveState()
                self.SaveState.run(FSM=self, char=k)

            if self.MBC.value[3] == 1:

                self.RemoveState = RemoveState()
                self.RemoveState.run(FSM=self, char=k)