import crawler.htmlparser as parser
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import pandas as pd
import random
import crawler.userlist as userlist
import pickle


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def get_basic_info(userid):
    """
    Gets the book titles, ids and ratings for a user.
    :param userid: The id of the user.
    :return: A list of tuples (title, id, rating)
    """

    try:
        books, num_books = parser.list_books(userid)

        if books == "Page does not exist":
            print("User does not exist.")
            return [("Page does not exist", userid, "na")]
        if books == "Profile is private":
            print("Profile is private.")
            return [("Profile is private", userid, "na")]
        if books == "Empty User":
            print("User has no books. What a loser.")
            return [("Empty User", userid, "na")]

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
        print("Cannot process this user?")
        return [("Cannot process user", userid, "na")]


def crawl_and_save(userlist_name):
    """
    Crawls forever, and saves the data to the extracted data folder.
    We can stop it and it will start where it left off.
    (Though it will skip the user we were just on because it will think
    we got their data. Our data set is big enough that this should not
    be a real issue.)
    :param userlist_name:
    :return: "Finished" if finished.
    """

    # Load data. If no file exists then start with empty list.
    try:
        data = pickle.load(open("extracted_data/" + userlist_name + "_data", "rb"))
    except:
        data = []

    userid = None

    while userid != "Finished":
        userid = userlist.next_user(userlist_name)
        info = get_basic_info(userid)

        data.append((userid, info))

        print("Saving data...")

        pickle.dump(data, open("extracted_data/" + userlist_name + "_data", "wb+"))

        print("Data Saved. \n")

    # If we somehow finish.
    pickle.dump(data, "extracted_data/" + userlist_name + "_data_finished")
    print("Extraction finished!?")
    return "Finished"


crawl_and_save("userlist_0")
