"""
The librarian saves books to the bookshelf if we do not have them already.
"""

import crawler.general as general
import shelve
import time
import os

USERLIST = "userlist_4"  # Change this to correct userlist and run the librarian.

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

# Open bookshelf
genre_db = shelve.open("book_db/bookshelf.db")


def gather_books(userlist_name):
    """
    Fetches the genres of books and makes a gid:genre entry in genre_db.
    :param userlist_name: Name of userlist to gather from.
    :return: None
    """
    path = None
    i = 0
    while path != "Finished":
        path = get_list(userlist_name, i)
        gather_from_file(path)
        genre_db["processed files"][path] = path
        i += 1
        general.print_("-------------- \nWe have completed {}! \n --------------- ".format(path))

    print("Finished gathering from {}".format(userlist_name))
    genre_db.close()


def get_list(userlist_name, i):
    """
    Get the next chunk of the list for the userlist name.
    :param userlist_name: Name of userlist
    :return: path to the chunk
    """

    filenames = os.listdir("extracted_data/{}_data".format(userlist_name))
    filename = filenames[i]
    if filename not in genre_db["processed files"]:
        path = "extracted_data/{}_data/{}".format(userlist_name, filename)
        return path

    return "Finished"


def gather_from_file(path):
    """
    Fetch the books in a user file and place them in the bookshelf.
    :param path: path to user file
    :return: None
    """

    if path not in genre_db["processed files"]:

        general.print_("Opening {}".format(path))

        l = general.read(path)

        for i in range(0, len(l)):
            user = l[i]
            fetch_books(user)

    else:
        general.print_("We have already processed {}".format(path))


def fetch_books(user):
    """
    Get the goodreads book objects for the user.
    :param user:
    :return:
    """

    books = []

    for book in user.userbooks:
        general.print_("\n{}".format(book.title))
        gather_book(book.goodreads_id)

    return books


def gather_book(goodreads_id):
    """
    Gathers a book with the goodreads id.
    :param goodreads_id: Book id to gather.
    :return: None
    """

    try:

        if not str(goodreads_id) in genre_db:

            start = time.time()

            general.print_("Downloading information...")
            book = goodreads.book(goodreads_id)

            # Make sure to not query goodreads more than once a second.
            end = time.time()
            total_time = end - start
            if 1 > total_time > 0:
                time.sleep(1 - total_time)

            add_to_bookshelf(book)

            general.print_("Book saved!")

        else:
            general.print_("Book is already in the bookshelf!")

    except:
        general.print_("Cannot process book. Skipping.")


def add_to_bookshelf(book):
    """
    Add a book to the bookshelf
    :param book: A goodreads book object
    :return: None
    """

    genre_db[str(book.gid)] = book

    genre_db["total books"] = genre_db["total books"] + 1


if __name__ == "__main__":
    gather_books(USERLIST)
