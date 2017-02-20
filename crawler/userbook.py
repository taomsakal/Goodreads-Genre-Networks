class UserBook:
    """
    An object to store the book data and the user's
    rating, etc of the book
    """

    def __init__(self):
        self.book = None  # The book object
        self.goodreads_id = "No gid"

        self.rating = "No rating"
        self.readcount = 0

        self.date_added = "No added date"
        self.date_purchased = "No purchase date"
        self.owned = "No owned info"
        self.purchase_location = None
        self.condition = None
        self.format = None
        self.review = None
        self.recomender = None
        self.notes = None
        self.comments = None
        self.votes = None
        self.date_pub_edition = None
        self.link = None
