import random
import pickle

import math


class UserList:
    """
    A list of users in a random order
    """

    def __init__(self, file_name, size):
        self.file_name = file_name
        self.size = size

        self.current_position = None


def make_and_save_list(num_chunks, name):
    """
    Makes and saves a list of all the user ids on goodreads in a random order.
    It the splits into n chunks, allowing us to run different lists on different
    computers.
    This is located in the file userlist_n
    :param num_chunks: size of each chunk
    :param name: The name of the file to create
    :return: None
    """

    size = 64962100  # This is about the number of users on Goodreads
    userlist = list(range(1, size))
    random.shuffle(userlist)

    userlists = chunkify(userlist, num_chunks)

    for i in list(range(0, len(userlists))):
        pickle.dump(userlists[i], open(name + "_{}".format(i), "wb+"))  # Save the list with teh number as a suffix


def chunkify(list_, n):
    """
    Divides list into n equal chunks.
    Stolen from the internet.
    :return: List of cut of lists
    """
    avg = len(list_) / float(n)
    out = []
    last = 0.0

    while last < len(list_):
        out.append(list_[int(last):int(last + avg)])
        last += avg

    return out


def load_file(name):
    """
    Loads the file.
    Path automatically appended to be userlist_db
    :param name:
    :return:
    """

    return pickle.load(open("userlist_db/" + name, 'rb'))


def next_user(filename):
    """
    Gets the next user from the user file.
    Then increments the counter.
    :param filename: Name of the file.
    :return: A user id
    """

    l = load_file(filename)
    counter = load_file(filename + "_counter")

    print("Getting next user. (We are at position {} in {}.)".format(counter, filename))

    pickle.dump(counter + 1, open("userlist_db/" + filename + "_counter", "wb+"))

    try:
        return l[counter]
    except:
        return "Finished"
