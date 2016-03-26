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


def loss(x, y):
    """
    :param x: last layer neurons output
    :param y: last history record
    :return:
    """
    return 0


def activation(x, max_loss):
    """
    :param x: last layer neurons output

    0 -lower bound
    1 -upper bound

    logistic/sigmoid function
    :return:
    """
    g = [y for y in x if y[1] == 'strength']
    y = [y for y in x if y[1] == 'worry']
    z = [y for y in x if y[1] == 'rationality']
    # print(g,y,z)
    # print(((g[0][0] + y[0][0]) - z[0][0]), max_loss)
    if ((g[0][0] + y[0][0]) - z[0][0]) > max_loss:
        return True, math.floor(g[0][0] + y[0][0]) - z[0][0]
    else:
        return False, math.floor(g[0][0] + y[0][0]) - z[0][0]


# def sigma(x):
#     return 1/(1+(math.exp(x)))