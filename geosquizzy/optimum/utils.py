import math


def diversity_factor(seqs, all_seqs_counts, biggest_seq_counts):
    """
    :param seqs: int()
    :param all_seqs_counts: int()
    :param biggest_seq_counts: int()
    :return: Diversity Factor
    """
    x = (biggest_seq_counts * 100) / all_seqs_counts
    return (x - (100-x)) / seqs


def growth_of_diversity(new, previous):
    """
    :param new: int(Diversity Factor)
    :param previous: int(Diversity Factor)
    :return: int (Growth of Diversity)
    increase if x -> -oo
    decrease if x -> +oo
    """
    return new - previous


def strength_of_measurement(current, total):
    """

    :param current: int() checked objects for new optimization procedure
    :param total: int() total objects available in doc (this is approximation)
    :return: int()
    """
    return (current * 100) / total


def loss():
    pass


def activation():
    pass


# def sigma(x):
#     return 1/(1+(math.exp(x)))