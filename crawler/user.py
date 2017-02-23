import pandas

from crawler import htmlparser as parser
from crawler.general import print_
from crawler.userbook import UserBook


class User:
    """
    Contains information about the user and
    all the userbooks they have.
    """

    def __init__(self):
        self.id = 0
        self.name = ""
        self.profile_type = "no type"  # Can be normal, restricted, private, empty, error or no type
        self.number_books = 0

        self.userbooks = []  # List of userbook objects
        self.dataframe = None
        self.username = "No Username"

    def make_userbook(self, htmlbook):
        """
        Makes a userbook object.
        :param htmlbook: The html of the book
        :return: Userbook object
        """

        userbook = UserBook()

        # Core information
        userbook.title = parser.extract_title(htmlbook)
        userbook.rating = parser.extract_user_rating(htmlbook)
        userbook.goodreads_id = parser.extract_goodreads_id(htmlbook)
        userbook.readcount = parser.extract_read_count(htmlbook)


        # Not-so-core information
        userbook.link = parser.extract_link(htmlbook)
        userbook.format = parser.extract_book_format(htmlbook)
        userbook.comments = parser.extract_comments(htmlbook)
        userbook.condition = parser.extract_book_condition(htmlbook)
        userbook.date_added = parser.extract_date_added(htmlbook)
        userbook.date_pub_edition = parser.extract_date_pub_edition(htmlbook)
        userbook.date_purchased = parser.extract_date_purchased(htmlbook)
        userbook.owned = parser.extract_owned(htmlbook)
        userbook.purchase_location = parser.extract_purchase_location(htmlbook)
        userbook.review = parser.extract_review(htmlbook)
        userbook.recommender = parser.extract_recommender(htmlbook)
        userbook.notes = parser.extract_notes(htmlbook)
        userbook.votes = parser.extract_votes(htmlbook)

        return userbook

    def build_dataframe(self):
        """
        Makes a dataframe for the user.
        :return: A pandas dataframe
        """

        print_("Building Dataframe...")

        try:

            # Init lists
            titles = []
            ratings = []
            goodreads_ids = []
            readcounts = []
            links = []
            formats = []
            comments = []
            conditions = []
            dates_added = []
            dates_pub_edition = []
            dates_purchased = []
            owned = []
            purchase_locations = []
            reviews = []
            recommenders = []
            notes = []
            votes = []

            for u in self.userbooks:
                titles.append(u.title)
                ratings.append(u.rating)
                goodreads_ids.append(u.goodreads_id)
                readcounts.append(u.readcount)
                links.append(u.link)
                formats.append(u.format)
                comments.append(u.comments)
                conditions.append(u.condition)
                dates_added.append(u.date_added)
                dates_pub_edition.append(u.date_pub_edition)
                dates_purchased.append(u.date_purchased)
                owned.append(u.owned)
                purchase_locations.append(u.purchase_location)
                reviews.append(u.review)
                recommenders.append(u.recommender)
                notes.append(u.notes)
                votes.append(u.votes)

            self.dataframe = pandas.DataFrame(
                data={"Title": titles, "Rating": ratings, "Goodreads ID": goodreads_ids, "Read Count": readcounts,
                      "Link": links, "Format": formats, "Comments": comments, "Condition": conditions,
                      "Date Added": dates_added, "Date Edition Published": dates_pub_edition,
                      "Date Purchased": dates_purchased,
                      "Owned": owned, "Purchase Location": purchase_locations, "Review": reviews,
                      "Recommender": recommenders, "Notes": notes, "Votes": votes})

            return self.dataframe

        except:

            print_("Failed to build dataframe.")
            return None
