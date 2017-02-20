from crawler.userbook import UserBook
from crawler import htmlparser as parser

class User:
    """
    Contains information about the user and
    all the userbooks they have.
    """

    def __init__(self):
        self.id = 0
        self.name = ""
        self.profile_type = "Normal"
        self.number_books = 0

        self.userbooks = []  # List of userbook objects

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
        userbook.recomender = parser.extract_recommender(htmlbook)
        userbook.notes = parser.extract_notes(htmlbook)
        userbook.votes = parser.extract_votes(htmlbook)

        return userbook

    def dataframe(self):
        """
        Makes a dataframe for the user.
        :return: A pandas dataframe
        """

        pass
