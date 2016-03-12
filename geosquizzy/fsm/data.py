import re

from geosquizzy.fsm.utils import create_unique_id
from geosquizzy.classes import Stack


class AnatomyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DataPortFiniteStateMachine:

    def __init__(self, *args, **kwargs):
        """
        :param kwargs['structure']: FeaturesTree Class
        """
        self.structure = kwargs.get('structure', None)
        self.data = None
        self.words = []
        self.values = []
        self.key = ''

    def extend_key(self, char=None):
        if char != '\n':
            self.key += char

    def add_word(self):
        self.words.append(re.sub('"', '', self.key))

    def remove_word(self):
        try:
            self.words.pop()
        except IndexError:
            pass

    def add_value(self):
        self.values.append(re.sub('"', '', self.key))

    def clean_values(self):
        self.values = []

    def save_value(self):
        self.structure.add_leaf_values(
            leaf_id=create_unique_id(self.words, 1),
            leaf_values=self.values)
        self.key = ''

    def save_word(self):
        node = self.structure.prepare_new_leaf(id=create_unique_id(self.words, 1),
                                               name=self.words[-1],
                                               level=self.words.__len__(),
                                               parent=create_unique_id(self.words, 0))
        self.structure.add_leaf(leaf=node)
        self.key = ''


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