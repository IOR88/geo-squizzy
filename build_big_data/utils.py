import random
import string

STRING_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_random_number(arg1, arg2):
    return int(random.uniform(arg1, arg2))


def get_random_string(size=0):
    return ''.join(random.choice(STRING_CHARS) for _ in range(size))