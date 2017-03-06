import random

from crawler.general import read, overwrite

GOODREADS_SIZE = 64962100  # Number of users in goodreads


def make_userlist_database(name, size, num_chunks):
    """
    Makes a userlist database which we can iterate through to get users. The counters
    remember our place in the list.
    WARNING: This will reset current userlists and counters by the same name.
    :param name: Name of files
    :param num_chunks: Number of files to split this into.
    :return: None
    """

    make_and_save_list(num_chunks, size, name)
    reset_counters(name, num_chunks)


def make_and_save_list(num_chunks, size, name):
    """
    Makes and saves a list of all the user ids on goodreads in a random order.
    It the splits into n chunks, allowing us to run different lists on different
    computers.
    This is located in the file userlist_n
    :param num_chunks: size of each chunk
    :param name: The name of the file to create
    :return: None
    """

    size = size  # This is about the number of users on Goodreads
    userlist = list(range(1, size))
    random.shuffle(userlist)

    userlists = chunkify(userlist, num_chunks)

    for i in list(range(0, len(userlists))):
        overwrite(userlists[i], name + "_{}".format(i))  # Save the list with teh number as a suffix


def reset_counters(name, n):
    """
    Reset the first n counters of name.
    :param name: The file name (without suffix)
    :param n: the number of counters to reset
    :return: None
    """

    for i in list(range(0, n)):
        overwrite(int(0), name + "_{}_counter".format(i))




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


def load_file(name, path="userlist_db/"):
    """
    Loads the file.
    Path automatically appended to be userlist_db
    :param name:
    :return:
    """

    return read(path + name)


def next_user(filename, path="userlist_db/"):
    """
    Gets the next user from the user file.
    Then increments the counter.
    :param filename: Name of the file.
    :return: A user id
    """

    l = load_file(filename, path=path)
    counter = load_file(filename + "_counter", path=path)

    print("Getting next user. (We are at position {} in {}.)".format(counter, filename))

    overwrite(counter + 1, path + filename + "_counter")

    try:
        return l[counter]
    except:
        return "finished"
