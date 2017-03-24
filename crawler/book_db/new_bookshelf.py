import shelve


def new_bookshelf(name):
    """
    Builds a new bookshelf, which is a python shelves object.
    :return: None
    """

    s = shelve.open('{}.db'.format(name))

    # Set the userlist name and counter to default values.
    s["last userlist_name"] = "No name"
    s["last userlist_counter"] = 0
    s["processed files"] = []
    s["total books"] = 0

    s.close()


# Run this to reset the bookshelf information.
# May not reset everything...
###new_bookshelf("amazon_bookshelf")
