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
            self.states[str(old)].deallocate()


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
            cls.collector.add(state=cls.instance, key=cls.instance.__name__())

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

                if char == '-' or char.isdigit():
                    FSM.command = FSM.Com.get_command(command=FSM.command, char=FSM.command[0] + 'DIG',
                                                      mbc=FSM.MBC.value.index(1))
                    FSM.MBC['value'] = FSM.command[2]
                else:
                    FSM.command = FSM.Com.get_command(command=FSM.command, char=FSM.command[0] + char,
                                                      mbc=FSM.MBC.value.index(1))
                    FSM.MBC['value'] = FSM.command[2]

            elif FSM.command[0] == 'ARR':

                if char == '-' or char.isdigit():
                    FSM.command = FSM.Com.get_command(command=FSM.command, char=FSM.command[0] + 'DIG',
                                                      mbc=FSM.MBC.value.index(1))
                    FSM.MBC['value'] = FSM.command[2]
                else:
                    FSM.command = FSM.Com.get_command(command=FSM.command, char=FSM.command[0] + char,
                                                      mbc=FSM.MBC.value.index(1))
                    FSM.MBC['value'] = FSM.command[2]

        else:
            FSM.command = FSM.Com.get_command(command=FSM.command, char=char,
                                              mbc=FSM.MBC.value.index(1))
            FSM.MBC['value'] = FSM.command[2]


class WriteState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)
        self.exp_quot_mar = 0

    def __name__(self):
        return '1'

    def run(self,  FSM=None, char=None):

        if FSM.command[0] == 'EXP':

            if char == '"':
                self.exp_quot_mar += 1

            if self.exp_quot_mar > 0:
                FSM.DataPort.extend_key(char=char)

            if self.exp_quot_mar == 2:
                FSM.MBC['value'] = [0, 0, 1, 0]

        elif FSM.command[0] == 'DIG':

            if FSM.command[1] == '11':

                if char == ',':
                    FSM.DataPort.add_value()
                    FSM.DataPort.key = ''

                elif char == ']':
                    FSM.DataPort.add_value()
                    FSM.DataPort.key = ''
                    FSM.MBC['value'] = [0, 0, 1, 0]

                else:
                    FSM.DataPort.extend_key(char=char)

            elif FSM.command[1] == '01':

                if char == ',':
                    FSM.DataPort.add_value()
                    FSM.key = ''
                    FSM.MBC['value'] = [0, 0, 1, 0]

                elif char == '}':
                    FSM.DataPort.add_value()
                    FSM.key = ''
                    FSM.MBC['value'] = [0, 0, 1, 0]

                else:
                    FSM.DataPort.extend_key(char=char)


class SaveState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)

    def __name__(self):
        return '2'

    def run(self,  FSM=None, char=None):

        if FSM.command[0] == 'EXP':

            if FSM.command[1] == '01':
                FSM.DataPort.add_word()
                FSM.DataPort.save_word()
                FSM.command = FSM.initial_state()
                FSM.MBC['value'] = FSM.command[2]

            elif FSM.command[1] == '10':
                FSM.DataPort.add_value()
                FSM.DataPort.save_value()
                FSM.command = FSM.initial_state()
                FSM.MBC['value'] = FSM.command[2]

        elif FSM.command[0] == 'DIG':

            if FSM.command[1] == '11':
                FSM.DataPort.save_value()
                FSM.command = FSM.initial_state()
                FSM.MBC['value'] = FSM.command[2]

            elif FSM.command[1] == '01':
                FSM.DataPort.save_value()

                if char == ',':
                    FSM.command, FSM.MBC['value'] = ('DEL', '01', [0, 0, 0, 1]), [0, 0, 0, 1]

                elif char == '}':
                    FSM.command, FSM.MBC['value'] = ('DEL', '11', [0, 0, 0, 1]), [0, 0, 0, 1]


class RemoveState(State):

    def __init__(self, *args, **kwargs):
        State.__init__(self)

    def __name__(self):
        return '3'

    def run(self,  FSM=None, char=None):

        if FSM.command[0] == 'DEL':

            if FSM.command[1] == '01':
                FSM.DataPort.remove_word()
                FSM.DataPort.clean_values()
                FSM.command = ('EXP', '01', [0, 1, 0, 0])
                FSM.MBC['value'] = [0, 1, 0, 0]

            elif FSM.command[1] == '11':
                try:
                    if FSM.DataAnatomy.peek() != 1:
                        FSM.DataPort.remove_word()
                        FSM.DataPort.clean_values()
                except IndexError:
                    FSM.DataPort.remove_word()
                    FSM.DataPort.clean_values()
                FSM.command = FSM.initial_state()
                FSM.MBC['value'] = FSM.command[2]