import random
import pickle


class UserList:
    """
    This creates a randomized list of user ids to crawl.
    Save this list and our position in it for future reference
    """

    def __init__(self):

        self.size = 64962100  # This is about the number of users on Goodreads

        self.current_position = 0

        self.list = list(range(0, self.size))
        random.shuffle(self.list)  # Shuffles the list in place






