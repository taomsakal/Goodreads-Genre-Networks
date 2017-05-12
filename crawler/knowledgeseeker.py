"""
The librarian gets books from the userlist, fetches information for the books, and then
saves it to a bookshelf (a python shelves object)
"""

import crawler.general as general
import shelve
from goodreads import client
from goodreads.book import GoodreadsBook
from amazon.api import AmazonAPI
import time
import os


class KnowledgeSeeker:
    def __init__(self, api_info, api_type='goodreads'):
        """
        Inits a knowledgeSeeker who will seek out book information.
        :param userlist_name: Name of userlist to get books from.
        :param api_info: key info for the api we are using. This is (key, secret) for goodreads
        and (amazon_access_key, amazon_secret_key, amazon_assoc_tag) for amazon.
        :param api_type: 'goodreads' or 'amazon'. The first gets book objects from goodreads
        and the second gets book objects from amazon.
        """

        self.api_type = api_type
        self.current_path = None

        if api_type == 'goodreads':
            self.api_client = client.GoodreadsClient(api_info[0], api_info[1])
            self.bookshelf_path = "../data/book_db/goodreads_bookshelf.db"
        else:
            raise Exception("api_type must be \'goodreads\'.")

        self.bookshelf = shelve.open(self.bookshelf_path)

    def gather_knowledge(self, userlist_name):
        """
        Fetches books from Goodreads and places them in the bookshelf database.
        :param userlist_name: Name of userlist to gather from.
        :return: None
        """

        path = None
        i = 0
        while path != "Finished":
            path = self.get_book_list(userlist_name, i)
            self.current_path = path
            self.gather_from_file(path)

            i += 1
            general.print_("-------------- \nWe have completed {}! \n --------------- ".format(path))

        print("Finished gathering from {}".format(userlist_name))

    def get_book_list(self, userlist_name, i):
        """
        Get the next chunk of the list for the userlist name.
        :param userlist_name: Name of userlist
        :return: path to the chunk
        """

        filenames = os.listdir("../data/userlists")

        try:
            filename = filenames[i]
            path = "../data/userlists/{}".format(filename)
            return path
        except IndexError:
            general.print_("Finished with {}".format(userlist_name))

    def gather_from_file(self, path):
        """
        Fetch the books in a user file and place them in the bookshelf.
        :param path: path to user file
        :return: None
        """

        general.print_("Opening {}".format(path))

        l = general.read(path)

        for i in range(0, len(l)):
            user = l[i]
            self.fetch_books(user)

    def fetch_books(self, user):
        """
        Get the goodreads book objects for the user.
        :param user:
        :return:
        """

        books = []

        for book in user.userbooks:
            general.print_("\n{}".format(book.title))
            self.gather_book(book)

        return books

    def gather_book(self, book, open_bookshelf=False):
        """
        Gathers an amazon or goodreads book.
        :param book: Book object
        :return: None
        """

        try:

            if str(book.goodreads_id) not in self.bookshelf or self.bookshelf[str(book.goodreads_id)] == "Skipped":
                if self.api_type == "goodreads":
                    downloaded_book = self.download_goodreads_book(book.goodreads_id)
                else:
                    raise Exception("api_type must be goodreads.")

                self.add_to_bookshelf(downloaded_book)

            else:
                general.print_("Book is already in the bookshelf!")

        except:
            general.print_("Cannot process book.")

    def add_to_bookshelf(self, book):
        """
        Add a book to the bookshelf
        :param book: A goodreads book object
        :return: None
        """

        if isinstance(book, GoodreadsBook):
            self.bookshelf[str(book.gid)] = book
            self.bookshelf.sync()

            general.print_("Book saved!")

    def download_goodreads_book(self, goodreads_id):
        """
        Download a goodreads book object.
        :return: goodreads book object
        """

        start = time.time()

        general.print_("Currently on {}".format(self.current_path))
        general.print_("Downloading information...")
        book = self.api_client.book(goodreads_id)

        # Make sure to not query goodreads more than once a second.
        end = time.time()
        total_time = end - start
        if 1 > total_time > 0:
            time.sleep(1 - total_time)

        return book
