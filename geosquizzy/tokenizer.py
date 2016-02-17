"""
@TOKENS -> dict() which contains all values that can occur during tokenizing process
@GRAMMAR_RULES -> dict() which contains some grammars(some specific relationships between tokens which
                         always occur, there are not individual cases)
"""

TOKENS = {
    'VALUE': r'[\w,\d]',
    'COMMA': r'[,]',
    'COLON': r'[:]',
    'QUOTATION_MARKS': r'["]',
    'WHITE_SPACE': r'[\s]',
    'SQUARE_BRACKET_O': r'[\[]',
    'SQUARE_BRACKET_E': r'[]]',
    'CURLY_BRACKET_O': r'[\{]',
    'CURLY_BRACKET_E': r'[}]',
}

SEQUENCES = {
    'KEY_O': r'[,]+[\{]+["]+|[\{]+["]+',
    'KEY_E': r'[:]+[\s]*["]+'
}

#TODO priorities of sequnces, tokesn ?

test_full_features = \
       '[{"geometry": ' \
       '{"type": "Point", "coordinates": [-122.93770201248995, 146.32791746493376]}, ' \
       '"properties": {"code": 4402, "name": "BZgtQyEu", "citizens": 351641, "country": "WKyCMBr"}, ' \
       '"type": "Feature"}]'

# TODO we need some way to create generator which would yield each time when some node was completed, so we can
# TODO send a ready to go search key to user


class JsonTokenizer:
    """
    usage -> for now we assume that a string represents full geojson
             features array in string format
    name  -> JsonTokenizer
    """
    def __init__(self, *args, **kwargs):
        """
        kwargs['structure'] -> instance of class FeaturesTree
                self.structure and self.tree from class GeoJSON now have the same
                reference point

        self.STATUS ->Integer() would mean which grammar rule was applied and
                                when status is 0 could mean that there is no
                                grammar rule currently applied
        """
        self.structure = kwargs['structure']
        self.tokens = TOKENS
        self.sequences = SEQUENCES
        self.STATUS = 0

    # GRAMMAR_RULES #
    def root_rule(self):
        """
        if first char is '['
        we open feature json array

        we are omitting meet char no status is set
        :return:
        """
        pass

    def nested_rule(self):
        self.STATUS = 2

    def key_rule(self):
        """
        if combination of chars ,{", {", was meet
        """
        self.STATUS = 3

    def value_rule(self):
        """
        if combination of chars :(?:[\s]*)", was meet
        it will end when char " is presented
        """
        self.STATUS = 4


