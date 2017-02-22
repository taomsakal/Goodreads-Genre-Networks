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
