from copy import deepcopy


class CommandsFiniteStateMachine:
    """
    FiniteStateMachine class commands, which are frozen for algorithm safety reasons,
    commands must be @immutable
    """

    def __init__(self, *args, **kwargs):
        self.commands = {
            '0{':      ('EXP', '01',   (0, 1, 0, 0)),
            '0:':      ('VAL', '0000', (1, 0, 0, 0)),
            '0,':      ('DEL', '01',   (0, 0, 0, 1)),
            '0}':      ('DEL', '11',   (0, 0, 0, 1)),
            '0]':      ('DEL', '11',   (0, 0, 0, 1)),
            '0VAL"':   ('EXP', '10',   (0, 1, 0, 0)),
            '0VALDIG': ('DIG', '01',   (0, 1, 0, 0)),
            '0VAL{':   ('EXP', '01',   (0, 1, 0, 0)),
            '0VAL[':   ('ARR', '10',   (1, 0, 0, 0)),
            '0ARR"':   ('EXP', '11',   (0, 1, 0, 0)),
            '0ARR{':   ('EXP', '01',   (0, 1, 0, 0)),
            '0ARRDIG': ('DIG', '11',   (0, 1, 0, 0))
        }

    def get_command(self, command=None, char=None, mbc=None):

        try:
            return deepcopy(self.commands[str(mbc) + char])
        except KeyError:
            return command