class StatesCollector:

    def __init__(self, *args, **kwargs):
        self.states = {}

    def add(self, state=None, key=None):
        self.states[key] = state

    def check(self, old_value=None, new_value=None):
        """
        check previous and actual state, if these are not equal in value comparison
        then previous state will be removed/deallocate
        """
        old = old_value.index(1)
        new = new_value.index(1)
        if old != new:
            self.states[old].deallocate()


class StateMeta(type):
    """
    StateMeta MetaClass keep reference to the same Class instance
    until deallocate class-method will be called
    """
    instance = None
    collector = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            collector = kwargs.get('collector', None)
            if not (collector is None):
                cls.collector = kwargs['collector']

            cls.instance = super(StateMeta, cls).__call__(cls, *args)
            cls.collector.add(state=cls.instance, key=cls.instance.__str__())

            return cls.instance
        else:
            return cls.instance

    # def __init__(cls, *args, **kwargs):
    #     super(Meta, cls).__init__(cls)
    #
    # def __new__(mcs, *args, **kwargs):
    #     return super(Meta, mcs).__new__(mcs, *args)


class State(metaclass=StateMeta):
    """
    State Class force all classes that inherits from it to define
    __name__ and run methods
    """

    @classmethod
    def deallocate(cls):
        cls.instance = None

    def __name__(self):
        """
        Name has to be an positive int and is used each time by StateMeta MetaClass when
        new instance of State Class is created, then StatesCollector as collector update its
        reference to new instance of called constructor
        """
        raise NotImplementedError

    def run(self,  FSM=None):
        """
        run method is executed within for loop of string in JSON format each time when its __name__ [0..N]
        is activated 0 > 1

        :param FSM: instance of GeojsonFiniteStateMachine Class
        :return:
        """
        raise NotImplementedError


class InterpretState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)

    def __name__(self):
        return '0'

    def run(self, FSM=None, char=None):
        if not (FSM.command[0] is None):
            if FSM.command[0] == 'VAL':
                # TODO TEMP DIGIT INTERPRET
                if char == '-' or char.isdigit():
                    FSM.command = FSM.Com.get_command(
                        char=FSM.command[0] + 'DIG', mbc=FSM.MBC.value.index(1))
                    FSM.MBC.value = FSM.command[2]
                else:
                    FSM.command = FSM.Com.get_command(
                        char=FSM.command[0] + char, mbc=FSM.MBC.value.index(1))
                    FSM.MBC.value = FSM.command[2]
            elif FSM.command[0] == 'ARR':
                # TODO TEMP DIGIT INTERPRET
                if char == '-' or char.isdigit():
                    FSM.command = FSM.Com.get_command(
                        char=FSM.command[0] + 'DIG', mbc=FSM.MBC.value.index(1))
                    FSM.MBC.value = FSM.command[2]
                else:
                    FSM.command = FSM.Com.get_command(
                        char=FSM.command[0] + char, mbc=FSM.MBC.value.index(1))
                    FSM.MBC.value = FSM.command[2]
        else:
            FSM.command = FSM.Com.get_command(char=char, mbc=FSM.MBC.value.index(1))
            FSM.MBC.value = FSM.command[2]


class WriteState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)
        self.exp_quot_mar = 0

    def __name__(self):
        return '1'

    def run(self,  FSM=None, char=None):
        # TODO FSM.__extend_key__(**kwargs)

        if FSM.command[0] == 'EXP':
            if char == '"':
                # open expression
                self.exp_quot_mar += 1
            if self.exp_quot_mar > 0:
                # saving expression
                # self.key += kwargs['char']
                FSM.__extend_key__(**kwargs)
            if self.exp_quot_mar == 2:
                # stop saving expression
                FSM.MBC.value = [0, 0, 1, 0]
        elif FSM.command[0] == 'DIG':
            if FSM.command[1] == '11':
                if char == ',':
                    FSM.__add_value__()
                    FSM.key = ''
                elif char == ']':
                    FSM.__add_value__()
                    FSM.key = ''
                    FSM.MBC.value = [0, 0, 1, 0]
                else:
                    FSM.__extend_key__(**kwargs)
            elif FSM.command[1] == '01':
                if char == ',':
                    FSM.__add_value__()
                    FSM.key = ''
                    FSM.MBC.value = [0, 0, 1, 0]
                elif char == '}':
                    FSM.__add_value__()
                    FSM.key = ''
                    FSM.MBC.value = [0, 0, 1, 0]
                else:
                    FSM.__extend_key__(**kwargs)


class SaveState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)

    def __name__(self):
        return '2'

    def run(self,  FSM=None, char=None):

        if FSM.command[0] == 'EXP':
                # save values " some expression "
            if FSM.command[1] == '01':
                # add key
                FSM.__add__word__()
                # save key
                FSM.__save__word__()
                FSM.command = FSM.__bring_fsm_initial_state()
                FSM.MBC.value = FSM.command[2]
            elif FSM.command[1] == '10':
                FSM.__add_value__()
                FSM.__save_value__()
                FSM.command = FSM.__bring_fsm_initial_state()
                FSM.MBC.value = FSM.command[2]

        elif FSM.command[0] == 'DIG':
            # save digits
            if FSM.command[1] == '11':
                FSM.__save_value__()
                # self.command[0], self.command[2], self.MBC = None, [1, 0, 0, 0], [1, 0, 0, 0]
                FSM.command = FSM.__bring_fsm_initial_state()
                FSM.MBC.value = FSM.command[2]
            elif FSM.command[1] == '01':
                FSM.__save_value__()
                if char == ',':
                    FSM.command, FSM.MBC = [
                        'DEL', '01', [
                            0, 0, 0, 1], 0], [
                        0, 0, 0, 1]
                elif char == '}':
                    FSM.command, FSM.MBC = [
                        'DEL', '11', [
                            0, 0, 0, 1], 0], [
                        0, 0, 0, 1]


class RemoveState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)

    def __name__(self):
        return '3'

    def run(self,  FSM=None, char=None):

        if FSM.command[0] == 'DEL':

            if FSM.command[1] == '01':
                FSM.__remove__word__()
                FSM.__clean__values__()
                # switch to write mode
                FSM.command = ['EXP', '01', [0, 1, 0, 0], 0]
                FSM.MBC.value = [0, 1, 0, 0]
            elif FSM.command[1] == '11':
                # will remove two words, because we are closing object
                try:
                    if FSM.DataAnatomy.peek() != '1':
                        FSM.__remove__word__()
                        FSM.__clean__values__()
                except IndexError:
                    FSM.__remove__word__()
                    FSM.__clean__values__()
                FSM.command = FSM.__bring_fsm_initial_state()
                FSM.MBC.value = FSM.command[2]