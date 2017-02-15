import pickle

"""
This makes and resets the counters.
"""


def reset_counters(name, n):
    """
    Reset the first n counters of name.
    :param name: The file name (without suffix)
    :param n: the number of counters to reset
    :return: None
    """

    for i in list(range(0, n)):
        pickle.dump(int(0), open(name + "_{}_counter".format(i), "wb+"))


reset_counters("userlist", 10)
