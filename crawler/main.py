import crawler.htmlparser as parser
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import pandas as pd
import random
import crawler.userlist as userlist
import pickle
from crawler.user import User, UserBook


def print_full_dataframe(x):
    """Prints a full dataframe"""
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def make_user(userid):
    """
    Make a user object, which holds information about the user along with all
    the books the user has. The books are stored as userbook objects
    :param userid: The id of the user.
    :return: a user object
    """

    books, num_books = parser.list_books(userid)  # Get information

    # Make user object and save information
    user = User()
    user.number_books = num_books
    user.profile_type = "normal"

    # Special user types
    if books == "Page does not exist":
        print("User does not exist.")
        user.profile_type = "does not exist"
        return user
    if books == "Profile is private":
        print("Profile is private.")
        user.profile_type = "private"
        return user

    # Display if user has no books
    if books == "Empty User":
        print("User has no books. What a loser.")

    for book in books:
        userbook = user.make_userbook(book)
        user.userbooks.append(userbook)

    return user

    # except:
    #     print("Cannot process this user?")
    #     return [("Cannot process user", userid, "na")]

def crawl_and_save(userlist_name, userlistpath="userlist_db/"):
    """
    Crawls forever, and saves the data to the extracted data folder.
    We can stop it and it will start where it left off.
    (Though it will skip the user we were just on because it will think
    we got their data. Our data set is big enough that this should not
    be a real issue.)
    :param userlist_name: Name of userlist file to crawl
    :return: "Finished" if finished.
    """

    # Load data. If no file exists then start with empty list.
    try:
        data = pickle.load(open("extracted_data/" + userlist_name + "_data", "rb"))
    except:
        data = []

    userid = None

    while userid != "Finished":
        userid = userlist.next_user(userlist_name, path=userlistpath)
        info = make_user(userid)

        data.append((userid, info))

        print("Saving data...")

        pickle.dump(data, open("extracted_data/" + userlist_name + "_data", "wb+"))

        print("Data Saved. \n")

    # If we somehow finish.
    pickle.dump(data, open("extracted_data/" + userlist_name + "_data_finished", "wb"))
    print("Extraction finished!?")
    return "Finished"


if __name__ == "__main__":
    crawl_and_save("userlist_2")
