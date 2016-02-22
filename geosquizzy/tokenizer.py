import re
import time
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
        self.LEVEL = 0

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

    def catch_key(self, data=None):
        word = ''
        for i, x in enumerate(data):
            #print(i, x)
            #assert False
            if not re.match(self.tokens['QUOTATION_MARKS'], x):
                word += x
            else:
                data = data[i+1:-1]
                break
        return word, data

    def run_tokenizer(self, data=None):
        start = time.time()
        words_list = []
        word = str()
        for i, x in enumerate(data):
            # if self.STATUS == 1 and not re.match(self.tokens['QUOTATION_MARKS'], x):
            #     word += x
            # if re.match(self.tokens['QUOTATION_MARKS'], x):
            #     if self.STATUS == 0:
            #         self.STATUS = 1
            #     elif self.STATUS == 1:
            #         #print(word, '\n')
            #         word = str()
            #         self.STATUS = 0
            if self.STATUS == 0 and re.match(self.tokens['CURLY_BRACKET_O'], x):
                """new json object"""
                self.STATUS = 1
            elif self.STATUS == 1 and re.match(self.tokens['QUOTATION_MARKS'], x):
                """json object key starting"""
                print(data.__len__())
                word, data = self.catch_key(data[i+1:-1])
                print(word, data.__len__(), data[0])
                # next option is
                # 1" VALUE "
                # 2{ nested value and we could go back to second if
                # 3[ which could have few possibilities
                    #1 [1123,12323] -> coordinates
                    #2 {} collection of objects
                    #3 [[],[]] collection of collectiond
                #assert False
                pass
        end = time.time()
        print(data.__len__())
        print(end-start)



