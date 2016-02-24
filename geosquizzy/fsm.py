"""
Geosquizzy Finite State Machine
@main core functionality of geosquizzy library
"""

"""
@States@
are functions which represent all possible GeojsonFiniteSateMachine states, each function
return next state to which transition should be made and 1||0 value which mean if transition should be made
or if the loop should go on in the current state waiting for a proper value so transition could have place

@kwargs
 @state
 @character
 @nestedness
"""


def S0(**kwargs):
    if kwargs['nestedness'] == 0 and kwargs['character'] == '[':
        return 1, "S1"
    else:
        return 0, None


def S1(**kwargs):
    if kwargs['character'] == '{':
        """
        new object starting
        """
        return 1, "S2"
    elif kwargs['character'] == '"' and not kwargs['super_flag']:
        """
        new key starting and previous char was '['
        """
        return 1, "S3"
    elif (kwargs['character'] == '"' or
          kwargs['character'] == '-' or
          kwargs['character'].isdigit()) and kwargs['super_flag']:
        """
        previous char was '[' if above condition is true, that's mean that
        values are array string or digits structure like: ["abc"...] or [10,2,-1...]
        """
        return 1, "S5"
    elif kwargs['character'] == '}':
        """
        object closing
        """
        return 1, "S6"
    else:
        return 0, None


def S2(**kwargs):
    if kwargs['nestedness'] >= 2 and kwargs['character'] == '"':
        return 1, "S3"
    else:
        return 0, None


def S3(**kwargs):
    if kwargs['nestedness'] >= 2 and kwargs['character'] == '"':
        return 1, "S4"
    else:
        return 0, None
    pass


def S4(**kwargs):
    if kwargs['nestedness'] >= 2 and kwargs['character'] == '[':
        """
        new array object
        """
        return 1, "S1"
    elif kwargs['nestedness'] >= 2 and kwargs['character'] == '}':
        """"
        object closing
        """
        return 1, "S6"
    elif kwargs['nestedness'] >= 2 and (kwargs['character'] == '"' or kwargs['character'].isdigit()):
        """"
        value pair for key object
        """
        return 1, "S5"
    elif kwargs['nestedness'] >= 2 and kwargs['character'] == '{':
        """"
        new nested value
        """
        return 1, "S2"
    else:
        return 0, None


def S5(**kwargs):
    if kwargs['nestedness'] >= 2 and kwargs['character'] == ']' and kwargs['super_flag']:
        return 1, "S1"
    elif kwargs['nestedness'] >= 2 and kwargs['character'] == '"' and not kwargs['super_flag']:
        return 1, "S1"
    elif kwargs['nestedness'] >= 2 and kwargs['character'] == ',' \
                                   and not kwargs['super_flag'] \
                                   and not kwargs['flag'] == 0:
        return 1, "S2"
    else:
        return 0, None


def S6(**kwargs):
    if kwargs['nestedness'] >= 2 and kwargs['character'] == ']':
        return 1, "SF"
    elif kwargs['nestedness'] >= 2 and kwargs['character'] == ',':
        return 1, "S1"
    else:
        return 0, None


def SF(**kwargs):
    """
    End state
    """
    return 0, None

"""
@Transitions@
are functions which are invoked during changing states, each function has access to
GeojsonFiniteStateMachine Instance and make changes to the machine body itself

META DATA
@transition level = 0...N A number of possible transition scenarios
"""


def S0T(instance=None, next_state=None):
    """@transition_level=1"""
    instance.nestedness += 1
    instance.state = next_state


def S1T(instance=None, next_state=None):
    """@transition_level=4"""
    instance.state = next_state
    if next_state == "S5":
        pass
    elif next_state == "S2":
        instance.nestedness += 1
        instance.super_flag = False
    elif next_state == "S3":
        instance.super_flag = False
    elif next_state == "S6":
        instance.words.pop()
        instance.nestedness -= 1


def S2T(instance=None, next_state=None):
    """@transition_level=1"""
    instance.state = next_state


def S3T(instance=None, next_state=None):
    """@transition_level=1"""
    instance.words.append(instance.key)
    instance.key = ''
    """update @self.structure model with new key"""
    node = instance.structure.prepare_new_leaf(id=instance.words[-1],
                                               level=instance.nestedness-1,
                                               parent=instance.words[-2])
    # print('NEW NODE', node, '\n')
    instance.structure.add_leaf(leaf=node)
    instance.state = next_state


def S4T(instance=None, next_state=None):
    """@transition_level=4"""
    instance.state = next_state
    if next_state == "S5":
        instance.flag = 0
    elif next_state == "S1":
        instance.super_flag = True
    elif next_state == "S6":
        instance.words.pop()
        instance.nestedness -= 1
    elif next_state == "S2":
        instance.nestedness += 1


def S5T(instance=None, next_state=None):
    """@transition_level=2(Two scenarios to the same S1 state)"""
    instance.state = next_state
    """restart flags"""
    instance.super_flag = False
    instance.flag = None
    """
    we can save example value for last leaf
    during this transition and we have to remove last key word
    """
    # print('ALL WORD', instance.words, '\n')
    # removed_word = instance.words.pop()
    instance.words.pop()
    instance.key = ''


def S6T(instance=None, next_state=None):
    """@transition_level=2"""
    instance.state = next_state
    if next_state == "S1":
        instance.nestedness += 1
    elif next_state == "SF":
        pass


def SFT(instance=None, next_state=None):
    """@transition_level=1"""
    """Ending Transition"""
    pass


class GeojsonFiniteStateMachine:
    def __init__(self, *args, **kwargs):
        """
        @kwargs['structure'] Nodes/Tree json keys model representation
        @self.nestedness is a dynamic factor +||- depending of json object nesting structure
        @self.states is a dict with functions, f() execution should return next state and 1||0
        @self.transitions is a list of tuples which represent all possible transition between states
        @self.flag as default None but can have few INTS
            [0 == "expression"("some expression between quotation marks")]
        """
        self.structure = kwargs['structure']
        self.nestedness = 0
        self.state = "S0"
        self.super_flag = False
        self.flag = None
        self.data = None
        self.words = ['root']
        self.key = ''
        self.states = {
            "S0": S0, "S1": S1, "S2": S2, "S3": S3, "S4": S4, "S5": S5,
            "S6": S6, "SF": SF
        }
        self.transitions = {
            "S0T": S0T, "S1T": S1T, "S2T": S2T, "S3T": S3T, "S4T": S4T, "S5T": S5T,
            "S6T": S6T, "SFT": SFT
        }

    def __pass_kwargs_to_states__(self, character):
        """
        :return prepared general body for states functions
        """
        return {"state": self.state, "character": character, "flag": self.flag,
                "nestedness": self.nestedness, "super_flag": self.super_flag}

    def run(self, **kwargs):
        """
        @kwargs['data'] features array
        """
        self.data = kwargs['data']
        for i, k in enumerate(self.data):
            # print(str(i)+' ', self.state, k, self.super_flag, self.nestedness)
            """activities depending on self.states"""
            if self.state == 'S3' and k != '"' and k != '\n':
                """joining key"""
                self.key += k
            elif self.state == 'S5' and k != '"' and k != '\n':
                """joining value"""
                self.key += k

            """loop logic"""
            bool_tuple = self.states[self.state](**self.__pass_kwargs_to_states__(k))
            if bool_tuple[0] == 1:
                """make transition to next state"""
                self.transitions[self.state+"T"](instance=self, next_state=bool_tuple[1])
            else:
                """keep going in current state"""
                pass
            #
            # if i == 2050:
            #     assert False