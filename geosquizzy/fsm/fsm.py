from geosquizzy.fsm.utils import (create_unique_id, WatchClass)
from geosquizzy.fsm.data import (DataPortFiniteStateMachine, DataAnatomyFiniteStateMachine)
from geosquizzy.fsm.commands import CommandsFiniteStateMachine
from geosquizzy.fsm.states import (StatesCollector, InterpretState, WriteState, SaveState, RemoveState)
from geosquizzy.fsm.selection import SelectionFiniteStateMachine


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
        @kwargs['percentage'] is an int
        """
        self.DataPort.data = kwargs['data']

        count = 0
        s_b = False

        DataSelection = None
        if kwargs.get('percentage', None):
            DataSelection = SelectionFiniteStateMachine(percentage=kwargs.get('percentage'),
                                                        len=self.DataPort.data.__len__())

        blocked = False



        # TODO PROFILING check enumerate and other for loop when going into prod
        for i, k in enumerate(self.DataPort.data):

            self.DataAnatomy.update_structure(char=k)
            # print(self.DataAnatomy.stack, i, k, '\n')

            if self.DataAnatomy.stack == [0, 1, 0]:
                if s_b is False:
                    count += 1
                    s_b = True
            elif self.DataAnatomy.stack == [0, 1]:
                s_b = False

            # TODO percentage traversing will extremely speed up whole process
            if DataSelection:
                blocked = DataSelection.run(anatomy=self.DataAnatomy.stack,
                                            blocked=blocked)

                if DataSelection.done():
                    break

            if not blocked:

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

        #     if i == 400:
        #         # TODO values for percentage 10
        #         print(DataSelection.visited_total)
        #         print(DataSelection.visited)
        #         print(DataSelection.to_visit)
        #         print(DataSelection.items)
        #         print(DataSelection.space)
        #         assert False
        # print(DataSelection.visited_total)
        # print(DataSelection.visited)
        # print(DataSelection.to_visit)
        # print(DataSelection.items)
        # print(DataSelection.space)
        # print(count)