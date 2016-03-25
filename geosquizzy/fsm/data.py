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

    # TODO PROFILING DataPortFiniteStateMachine extend_key

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
        exist = self.structure.add_leaf(leaf=node)
        self.key = ''
        return exist

    def sig_new(self, omitted=None):
        self.structure.new_obj(omitted)


class DataAnatomyFiniteStateMachine(Stack):

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        @body
        @self.values 0 {object} 1[array]
        """
        self.values = {'}': 0, ']': 1, '{': 0, '[': 1}
        self.result = None
        self.count = 0
        Stack.__init__(self, *args, **kwargs)

    # TODO PROFILING DataAnatomyFiniteStateMachine update_structure
    def update_structure(self, **kwargs):
        if kwargs['char'] in ['{', '[']:
            self.push(self.values[kwargs['char']])
        elif kwargs['char'] in ['}', ']']:
            rem = self.pop()

            if rem != self.values[kwargs['char']]:
                raise AnatomyError('GeoJSON syntax error ("not matching between opening and closing parenthesis")')

            if self.stack == [0, 1]:
                """
                This if statement is counting total amount of objects for now we assume that structure is an GeoJSON
                document, but after we will have to update it so it will be possible to handle any JSON structure
                """
                self.count += 1
                return True
        return False