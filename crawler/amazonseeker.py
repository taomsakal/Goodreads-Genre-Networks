from crawler.general import print_
import shelve
from amazon.api import AmazonAPI  #pip install python-amazon-simple-product-api
from crawler.api_data import aws
from crawler.amazonbook import AmazonBook
from goodreads.book import GoodreadsBook



class AmazonSeeker:
    def __init__(self):
        """
        Inits a knowledgeSeeker who will seek out book information.
        :param userlist_name: Name of userlist to get books from.
        :param api_info: key info for the api we are using. This is (key, secret) for goodreads
        and (amazon_access_key, amazon_secret_key, amazon_assoc_tag) for amazon.
        :param api_type: 'goodreads' or 'amazon'. The first gets book objects from goodreads
        and the second gets book objects from amazon.
        """

        # Init goodreads bookshelf
        # Make it read only so than can run goodreads book seeker in parallel
        self.source_bookshelf = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')

        # Init the bookshelf we will store amazon data in
        self.amazon_bookshelf = shelve.open("../data/book_db/amazon_bookshelf.db")

        # Init the amazon client.
        self.amazon = AmazonAPI(*aws)

    def gather(self, skipped=False):
        """
        Fetches books from Goodreads and places them in the bookshelf database.
        :param userlist_name: Name of userlist to gather from.
        :return: None
        """

        for key in self.source_bookshelf.keys():
            gbook = None
            try:
                gbook = self.source_bookshelf.get(str(key), default=None)
            except:
                print("Something Funny Happened")
            if isinstance(gbook, GoodreadsBook):
                if hasattr(gbook, "gid"):  # If is actually a book.
                    if gbook.gid not in self.amazon_bookshelf or gbook == "Skipped":

                        print_(gbook.title)

                        # Download amazon data
                        abook = self.download_amazon_book(gbook)

                        # turn into amazon book object
                        if abook != "Skipped":
                            abook = self.make_amazon_book(abook)

                        # Add to shelve
                        self.add_to_bookshelf(abook, gbook)
                    else:
                        print_(gbook.title)
                        print_("Already in bookshelf!\n")

    def add_to_bookshelf(self, abook, gbook, skipped=False):
        """
        Add a book to the bookshelf
        :param book: A goodreads book object
        :return: None
        """

        if abook != "Skipped":
            self.amazon_bookshelf[str(gbook.gid)] = abook
            print_("Data Saved!\n")
        else:
            self.amazon_bookshelf[str(gbook.gid)] = "Skipped"

    def download_amazon_book(self, gbook):
        """
        Downloads amazon book information
        :param book: book object
        :return: amazon book as a list
        """

        abook = None

        # Lookup via isbn
        try:
            print_("Looking up by isbn...")
            abook = self.amazon.lookup(IdType="ISBN", ItemId=str(gbook.isbn), SearchIndex='Books')
        except:

            # If above fails, lookup via isbn13
            try:
                print_("Failed isbn lookup. Trying isbn13...")
                abook = self.amazon.lookup(IdType="ISBN", ItemId=str(gbook.isbn13), SearchIndex='Books')
            except:

                # Finally, try a search and get first item
                try:
                    print_("Failed isbn13 lookup. Trying a search...")
                    abook = self.amazon.search_n(1, Power="author:{} and title:{}".format(gbook.authors, gbook.title),
                                                 SearchIndex='Books')

                except:
                    print_("Failed search. Skipping...\n")
                    return "Skipped"

        # Make sure return list of abooks
        if not isinstance(abook, list):
            abook = [abook]

        abook = self.pick_best(abook)

        return abook

    def pick_best(self, abook_list):
        """
        Pick the abook with the lowest sales rank (aka the highest selling)
        to decide which book to use when there are multiple.
        :param abook_list: List of abooks
        :return: A single abook
        """

        best = None
        for abook in abook_list:
            if best is None:
                best = abook

            try:
                if int(abook.sales_rank) < int(best.sales_rank):
                    best = abook
            except:  # If do not have sales rank then assume is infinity and skip
                pass

        print("Best sale rank: {}".format(best.sales_rank))

        return best

    def make_amazon_book(self, abook):
        """
        Makes an amazon book object from the downloaded information.
        Note that we do this because we cannot pickle the downloaded object directly.
        :param abook: Downloaded amazon book object.
        :return: amazon book object.
        """

        abook = AmazonBook(abook)

        print_("Genres: {}".format(abook.genres))

        self.amazon_bookshelf.sync()

        return abook


if __name__ == "__main__":
    seeker = AmazonSeeker()
    seeker.gather()
