from geosquizzy.fsm.utils import (create_unique_id, WatchClass)
from geosquizzy.fsm.data import (DataPortFiniteStateMachine, DataAnatomyFiniteStateMachine)
from geosquizzy.fsm.commands import CommandsFiniteStateMachine
from geosquizzy.fsm.states import (StatesCollector, InterpretState, WriteState, SaveState, RemoveState)
from geosquizzy.fsm.economize import EconomizeFiniteStateMachine
from multiprocessing import Process


class MBC(WatchClass):
    def __init__(self, *args, **kwargs):
        super(MBC, self).__init__(*args, **kwargs)


class GeojsonFiniteStateMachine:

    def __init__(self, *args, **kwargs):
        """
        :param kwargs['structure']: FeaturesTree Class
        """
        self.DataPort = DataPortFiniteStateMachine(structure=kwargs['structure'])
        self.ProgressQueue = kwargs.get('progress_queue')
        self.DataAnatomy = DataAnatomyFiniteStateMachine()
        self.Economization = EconomizeFiniteStateMachine()
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
        @kwargs['percentage'] is an int
        """
        self.DataPort.data = kwargs['data']

        exist = None

        for k in self.DataPort.data:
            increased = self.DataAnatomy.update_structure(char=k)

            if increased:
                self.DataPort.sig_new(omitted=self.Economization.omitted_obj)
                self.Economization.increase_progress()
                self.ProgressQueue.put(1)

            if not (exist is None):
                self.Economization.adjust_space(exist=exist)
                exist = None

            if self.Economization.economize():
                if increased:
                    self.Economization.omit()
            else:

                # TODO one process
                if self.MBC.value[0] == 1:

                    self.InterpretState = InterpretState()
                    self.InterpretState.run(FSM=self, char=k)

                if self.MBC.value[1] == 1:

                    self.WriteState = WriteState()
                    self.WriteState.run(FSM=self, char=k)

                if self.MBC.value[2] == 1:

                    self.SaveState = SaveState()
                    exist = self.SaveState.run(FSM=self, char=k)

                if self.MBC.value[3] == 1:

                    self.RemoveState = RemoveState()
                    self.RemoveState.run(FSM=self, char=k)

        self.ProgressQueue.put(0)
        self.ProgressQueue.join()