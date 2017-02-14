class UserBook:
    """
    An object to store the book data and the user's
    rating, etc of the book
    """

    def __init__(self):

        self.goodreads_id = 'no id'
        self.user_rating = 'no rating'
        self.owner = 'no owner'

class User:
    """
    Contains information about the user and
    all the userbooks they have.
    """

    def __init__(self):

        self.books = {}