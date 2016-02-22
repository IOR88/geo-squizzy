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
    if kwargs['nestedness'] == 1 and kwargs['character'] == '{':
        return 1, "S2"
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
    return 0, None


def S5(**kwargs):
    pass

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
    """@transition_level=1"""
    instance.nestedness += 1
    instance.state = next_state


def S2T(instance=None, next_state=None):
    """@transition_level=1"""
    instance.state = next_state


def S3T(instance=None, next_state=None):
    """@transition_level=1"""
    instance.words.append(instance.key)
    instance.key = ''
    """update @self.structure model with new key"""
    instance.state = next_state


def S4T(instance=None, next_state=None):
    pass


def S5T(instance=None, next_state=None):
    pass


class GeojsonFiniteStateMachine:
    def __init__(self, *args, **kwargs):
        """
        @kwargs['structure'] Nodes/Tree json keys model representation
        @self.nestedness is a dynamic factor +||- depending of json object nesting structure
        @self.states is a dict with functions, f() execution should return next state and 1||0
        @self.transitions is a list of tuples which represent all possible transition between states
        """
        self.structure = kwargs['structure']
        self.nestedness = 0
        self.state = "S0"
        self.data = None
        self.words = []
        self.key = ''
        self.states = {
            "S0": S0, "S1": S1, "S2": S2, "S3": S3, "S4": S4, "S5": S5
        }
        self.transitions = {
            "S0T": S0T, "S1T": S1T, "S2T": S2T, "S3T": S3T, "S4T": S4T, "S5T": S5T
        }

    def __pass_kwargs_to_states__(self, character):
        """
        :return prepared general body for states functions
        """
        return {"state": self.state, "character": character, "nestedness": self.nestedness}

    def run(self, **kwargs):
        """
        @kwargs['data'] features array
        """
        self.data = kwargs['data']
        for k in self.data:

            """activities depending on self.states"""
            if self.state == 'S3' and k != '"':
                """joining key"""
                self.key += k
            elif self.state == 'S4' and k != '"':
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