"""
A few general functions
"""

import pickle

import pandas


def print_(string, print_status=True):
    """
    Print the string if get_status is true
    :param string: string to print
    :return: None
    """

    if print_status:
        print(string)


def print_full(x):
    """
    Prints the full dataframe.
    """
    pandas.set_option('display.max_rows', len(x))
    print(x)
    pandas.reset_option('display.max_rows')


def overwrite(data, filename):
    """
    Saves the data to a file, overwriting previous data.
    """

    file = open(filename, "wb")
    pickle.dump(data, file)
    file.close()


def read(filename):
    """
    Read data from a file.
    :return: data in file
    """

    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()

    return data
