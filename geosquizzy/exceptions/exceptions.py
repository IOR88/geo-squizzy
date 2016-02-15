from exceptions.messages import MESSAGES


class FeatureSyntaxError(SyntaxError):
    def __init__(self):
        super(FeatureSyntaxError, self).__init__(MESSAGES['1'])


class FeatureStructureError(Exception):
    def __init__(self):
        super(FeatureStructureError, self).__init__(MESSAGES['2'])


class FeatureCoordinatesError(Exception):
    def __init__(self):
        super(FeatureCoordinatesError, self).__init__(MESSAGES['3'])