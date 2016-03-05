import re
import copy


class GeojsonFiniteStateMachine:
    # TODO create separation between fsm core logic and temp data usage/functionality
    def __init__(self, *args, **kwargs):
        """
        @kwargs['structure'] Nodes/Tree json keys model representation
        """
        self.structure = kwargs['structure']
        self.MBC = [0, 0, 0, 0]
        self.stack_structure = []
        self.command = [None, '0', [0, 0, 0, 0], -1]
        self.words = []
        self.values = []
        self.key = ''
        self.lib_commands = {
            '0{': ['EXP', '01', [0, 1, 0, 0], 0],
            '0:': ['VAL', '0000', [1, 0, 0, 0], 0],
            '0,': ['DEL', '01', [0, 0, 0, 1], 0],
            '0}': ['DEL', '11', [0, 0, 0, 1], 0],
            '0]': ['DEL', '11', [0, 0, 0, 1], 0],
            '0VAL"': ['EXP', '10', [0, 1, 0, 0], 0],
            '0VALDIG': ['DIG', '01', [0, 1, 0, 0], 0],
            '0VAL{': ['EXP', '01', [0, 1, 0, 0], 0],
            '0VAL[': ['ARR', '10', [1, 0, 0, 0], 0],
            '0ARR"': ['EXP', '11', [0, 1, 0, 0], 0],
            '0ARR{': ['EXP', '01', [0, 1, 0, 0], 0],
            '0ARRDIG': ['DIG', '11', [0, 1, 0, 0], 0]
        }

    def __create_unique_id__(self, key):
        """
        creating unique ids which represent keys in structure nodes, allow
        us to store the same key names but which exist on different levels of doc structure
        """
        if key == 0:
            'parent'
            try:
                name = self.words[-2]
                return name+str(self.words.__len__()-1)
            except IndexError:
                return None
        elif key == 1:
            'children'
            return self.words[-1]+str(self.words.__len__())

    def __get__command(self, char=None, mbc=None):
        """
        @:return one of command from lib_commands
        for security we added deepcopy, because somewhere in the code, the lib_commands
        because of reference was changed,
        """
        # TODO self.lib_commands should be immutable object, and all mutables should be placed in different structure
        try:
            return copy.deepcopy(self.lib_commands[mbc+char])
        except KeyError:
            return self.command

    def __modify_structure_stack__(self, **kwargs):
        if kwargs['arg'] == '[':
            self.stack_structure.append('ARR')
        elif kwargs['arg'] == '{':
            self.stack_structure.append('OBJ')
        elif kwargs['arg'] == ']' or kwargs['arg'] == '}':
            try:
                self.stack_structure.pop()
            except IndexError:
                pass

    def __bring_fsm_initial_state(self):
        return [None, '0', [1, 0, 0, 0], -1]

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
        self.structure.add_leaf_values(id=self.__create_unique_id__(1), values=self.values)
        self.key = ''

    def __save__word__(self):
        node = self.structure.prepare_new_leaf(id=self.__create_unique_id__(1),
                                               name=self.words[-1],
                                               level=self.words.__len__(),
                                               parent=self.__create_unique_id__(0))
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
                    self.command = self.__get__command(char=self.command[0]+'DIG', mbc='0')
                    self.MBC = self.command[2]
                else:
                    self.command = self.__get__command(char=self.command[0]+kwargs['char'], mbc='0')
                    self.MBC = self.command[2]
            elif self.command[0] == 'ARR':
                # TODO TEMP DIGIT INTERPRET
                if kwargs['char'] == '-' or kwargs['char'].isdigit():
                    self.command = self.__get__command(char=self.command[0]+'DIG', mbc='0')
                    self.MBC = self.command[2]
                else:
                    self.command = self.__get__command(char=self.command[0]+kwargs['char'], mbc='0')
                    self.MBC = self.command[2]
        else:
            self.command = self.__get__command(char=kwargs['char'], mbc='0')
            self.MBC = self.command[2]

    def __write__(self, **kwargs):
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
                    self.command, self.MBC = ['DEL', '01', [0, 0, 0, 1], 0], [0, 0, 0, 1]
                elif kwargs['char'] == '}':
                    self.command, self.MBC = ['DEL', '11', [0, 0, 0, 1], 0], [0, 0, 0, 1]

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
                    if self.stack_structure[-1] != 'ARR':
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
        self.data = kwargs['data']
        self.MBC[0] = 1

        for i, k in enumerate(self.data):
            # print(self.command, ' ', k, '  ', i)
            # print(self.words)
            # print('\n')
            self.__modify_structure_stack__(arg=k)

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