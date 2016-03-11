from geosquizzy.classes import Stack


class AnatomyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DataPortFiniteStateMachine:

    def __init__(self, *args, **kwargs):
        self.structure = kwargs.get('data', {})


class DataAnatomyFiniteStateMachine(Stack):

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        @body
        @self.options 1 opening 0 closing
        @self.values 0 {object} 1[array]
        """
        self.options = {'1':
                        {'match': ['{', '[']},
                        '0':
                        {'match': ['}', ']']}
                        }
        self.values = {'0': 0, '1': 1}
        self.result = None
        Stack.__init__(self, *args, **kwargs)

    def update_structure(self, **kwargs):
        if self.__match__(mode='1', char=kwargs['char']):
            self.push(self.result[0])
        elif self.__match__(mode='0', char=kwargs['char']):
            if not self.is_empty():
                if self.peek() == self.result[0]:
                    self.pop()
                else:
                    raise AnatomyError('GeoJSON syntax error ("not matching between opening and closing parenthesis")')

    def __match__(self, mode=None, char=None):
        try:
            index = self.options[mode]['match'].index(char)
        except ValueError:
            return False
        else:
            self.result = (self.values[str(index)],)
            return True