import crawler.htmlparser as parser
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import pandas as pd
import random


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

#books = parser.list_books(2419628)


def get_basic_info(userid):
    """
    Gets the book titles, ids and ratings for a user.
    :param userid: The id of the user.
    :return: A set of tuples (title, id, rating)
    """

    try:
        books, num_books = parser.list_books(userid)

        if books == "Page does not exist":
            return "Page does not exist", userid, "na"
        if books == "Profile is private":
            return "Profile is private", userid, "na"
        if books == "Empty User":
            return "Empty User", userid, "na"

        titles = []
        ids = []
        ratings = []

        for book in books:
            titles.append(parser.extract_title(book))
            ratings.append(parser.extract_user_rating(book))
            ids.append(parser.extract_goodreads_id(book))

        data = {"Title": titles, "Rating": ratings, "Goodreads ID": ids}
        dframe = pd.DataFrame(data)
        print_full(dframe)

        data = list(zip(titles, ids, ratings))
        return data


    except:
        return ("Cannot process user", userid, "na")


l = list(range(0, 55000))

random.shuffle(l)

for i in l:
    print(get_basic_info(i))


