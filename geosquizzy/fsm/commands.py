from copy import deepcopy


class CommandsFiniteStateMachine:
    """
    FiniteStateMachine class commands, which are frozen for algorithm safety reasons,
    commands must be @immutable
    """

    def __init__(self, *args, **kwargs):
        self.commands = {
            '00':      (None,  '0',    [1, 0, 0, 0]),  # starting and default command on interpret state
            '0{':      ('EXP', '01',   [0, 1, 0, 0]),
            '0:':      ('VAL', '0000', [1, 0, 0, 0]),
            '0,':      ('DEL', '01',   [0, 0, 0, 1]),
            '0}':      ('DEL', '11',   [0, 0, 0, 1]),
            '0]':      ('DEL', '11',   [0, 0, 0, 1]),
            '0VAL"':   ('EXP', '10',   [0, 1, 0, 0]),
            '0VALDIG': ('DIG', '01',   [0, 1, 0, 0]),
            '0VAL{':   ('EXP', '01',   [0, 1, 0, 0]),
            '0VAL[':   ('ARR', '10',   [1, 0, 0, 0]),
            '0ARR"':   ('EXP', '11',   [0, 1, 0, 0]),
            '0ARR{':   ('EXP', '01',   [0, 1, 0, 0]),
            '0ARRDIG': ('DIG', '11',   [0, 1, 0, 0])
        }

    def get_command(self, command=None, char=None, mbc=None):
        new_command = None
        try:
            new_command = self.commands[str(mbc) + char]
            # print('HELLO1')
        except KeyError:
            # print('HELLO2', command)
            new_command = command
            # print(new_command)
        finally:
            return new_command