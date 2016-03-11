import re

from geosquizzy.fsm.utils import create_unique_id
from geosquizzy.fsm.data import (DataPortFiniteStateMachine, DataAnatomyFiniteStateMachine)
from geosquizzy.fsm.commands import CommandsFiniteStateMachine
from geosquizzy.fsm.states import (interpret, write, save, remove)


class GeojsonFiniteStateMachine:
    # TODO migrate all states into

    def __init__(self, *args, **kwargs):
        """
        @kwargs['structure'] FeaturesTree Class
        """
        self.DataPort = DataPortFiniteStateMachine(data=kwargs['structure'])
        self.DataAnatomy = DataAnatomyFiniteStateMachine()
        self.Com = CommandsFiniteStateMachine()
        self.structure = kwargs['structure']
        self.MBC = [1, 0, 0, 0]
        self.command = self.Com.get_command(char='0', mbc=self.MBC.index(1))
        self.words = []
        self.values = []
        self.key = ''

    @staticmethod
    def __bring_fsm_initial_state():
        return None, '0', [1, 0, 0, 0]

    def __extend_key__(self, **kwargs):
        if kwargs['char'] != '\n':
            self.key += kwargs['char']

    def __add__word__(self):
        self.words.append(re.sub('"', '', self.key))

    def __remove__word__(self):
        try:
            self.words.pop()
        except IndexError:
            pass

    def __add_value__(self):
        self.values.append(re.sub('"', '', self.key))

    def __clean__values__(self):
        self.values = []

    def __save_value__(self):
        self.structure.add_leaf_values(
            leaf_id=create_unique_id(self.words, 1),
            leaf_values=self.values)
        self.key = ''

    def __save__word__(self):
        node = self.structure.prepare_new_leaf(id=create_unique_id(self.words, 1),
                                               name=self.words[-1],
                                               level=self.words.__len__(),
                                               parent=create_unique_id(self.words, 0))
        self.structure.add_leaf(leaf=node)
        self.key = ''

    def __interpret__(self, **kwargs):
        """
        :param kwargs: arg = character
        :return:None
        """
        if not (self.command[0] is None):
            if self.command[0] == 'VAL':
                # TODO TEMP DIGIT INTERPRET
                if kwargs['char'] == '-' or kwargs['char'].isdigit():
                    self.command = self.Com.get_command(
                        char=self.command[0] + 'DIG', mbc=self.MBC.index(1))
                    self.MBC = self.command[2]
                else:
                    self.command = self.Com.get_command(
                        char=self.command[0] + kwargs['char'], mbc=self.MBC.index(1))
                    self.MBC = self.command[2]
            elif self.command[0] == 'ARR':
                # TODO TEMP DIGIT INTERPRET
                if kwargs['char'] == '-' or kwargs['char'].isdigit():
                    self.command = self.Com.get_command(
                        char=self.command[0] + 'DIG', mbc=self.MBC.index(1))
                    self.MBC = self.command[2]
                else:
                    self.command = self.Com.get_command(
                        char=self.command[0] + kwargs['char'], mbc=self.MBC.index(1))
                    self.MBC = self.command[2]
        else:
            self.command = self.Com.get_command(char=kwargs['char'], mbc=self.MBC.index(1))
            self.MBC = self.command[2]

    def __write__(self, **kwargs):
        # TODO IndexError: tuple index out of range -> command does not have index 3 now, object was set to immutable type and
        # TODO and any mutable values were removed,
        """
        :param kwargs: arg = character
        :return:None
        """
        if self.command[0] == 'EXP':
            if kwargs['char'] == '"':
                # open expression
                self.command[3] += 1
            if self.command[3] > 0:
                # saving expression
                # self.key += kwargs['char']
                self.__extend_key__(**kwargs)
            if self.command[3] == 2:
                # stop saving expression
                self.MBC = [0, 0, 1, 0]
        elif self.command[0] == 'DIG':
            if self.command[1] == '11':
                if kwargs['char'] == ',':
                    self.__add_value__()
                    self.key = ''
                elif kwargs['char'] == ']':
                    self.__add_value__()
                    self.key = ''
                    self.MBC = [0, 0, 1, 0]
                else:
                    self.__extend_key__(**kwargs)
                    # self.key += kwargs['char']
            elif self.command[1] == '01':
                if kwargs['char'] == ',':
                    self.__add_value__()
                    self.key = ''
                    self.MBC = [0, 0, 1, 0]
                elif kwargs['char'] == '}':
                    self.__add_value__()
                    self.key = ''
                    self.MBC = [0, 0, 1, 0]
                else:
                    self.__extend_key__(**kwargs)
                    # self.key += kwargs['char']

    def __save__(self, **kwargs):
        """
        :param kwargs: arg = character
        :return:None
        """
        if self.command[0] == 'EXP':
                # save values " some expression "
            if self.command[1] == '01':
                # add key
                self.__add__word__()
                # save key
                self.__save__word__()
                self.command = self.__bring_fsm_initial_state()
                self.MBC = self.command[2]
            elif self.command[1] == '10':
                self.__add_value__()
                self.__save_value__()
                self.command = self.__bring_fsm_initial_state()
                self.MBC = self.command[2]

        elif self.command[0] == 'DIG':
            # save digits
            if self.command[1] == '11':
                self.__save_value__()
                # self.command[0], self.command[2], self.MBC = None, [1, 0, 0, 0], [1, 0, 0, 0]
                self.command = self.__bring_fsm_initial_state()
                self.MBC = self.command[2]
            elif self.command[1] == '01':
                self.__save_value__()
                if kwargs['char'] == ',':
                    self.command, self.MBC = [
                        'DEL', '01', [
                            0, 0, 0, 1], 0], [
                        0, 0, 0, 1]
                elif kwargs['char'] == '}':
                    self.command, self.MBC = [
                        'DEL', '11', [
                            0, 0, 0, 1], 0], [
                        0, 0, 0, 1]

    def __remove__(self, **kwargs):
        """
        :param kwargs: arg = character
        :return:None
        """
        if self.command[0] == 'DEL':

            if self.command[1] == '01':
                self.__remove__word__()
                self.__clean__values__()
                # switch to write mode
                self.command = ['EXP', '01', [0, 1, 0, 0], 0]
                self.MBC = [0, 1, 0, 0]
            elif self.command[1] == '11':
                # will remove two words, because we are closing object
                try:
                    if self.DataAnatomy.peek() != '1':
                        self.__remove__word__()
                        self.__clean__values__()
                except IndexError:
                    self.__remove__word__()
                    self.__clean__values__()
                self.command = self.__bring_fsm_initial_state()
                self.MBC = self.command[2]

    def run(self, **kwargs):
        """
        @kwargs['data'] features array
        @self.MBC[0] is set to 1 to run Interpret state as initial one
        """
        self.data = kwargs['data']  # TODO move to DataPort var
        self.MBC[0] = 1

        for i, k in enumerate(self.data):
            # print(self.command, ' ', k, '  ', i)
            # print(self.words)
            # print('\n')
            self.DataAnatomy.update_structure(char=k)

            if self.MBC[0] == 1:
                # interpret #
                self.__interpret__(char=k)
            if self.MBC[1] == 1:
                # write #
                self.__write__(char=k)
            if self.MBC[2] == 1:
                # save #
                self.__save__(char=k)
            if self.MBC[3] == 1:
                # delete #
                self.__remove__()

            if i == 330:
                # pass
                # print(self.structure.nodes)
                # TODO 282 should remove value
                # TODO 296 ? not removed words ?
                # TODO 322-323 key not added ?
                # assert False
                pass
