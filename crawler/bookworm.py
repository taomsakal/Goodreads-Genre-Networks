"""
This is the main crawler.
It takes users from the userlist and the book information from their read shelf.
It saves the data as a list of user objects in userlist_n_data.

To run: Change the USER_LIST variable below to the file to run. (Taom even, Rachel odd.)

If we abort, the process should pick up where it left off. Note that it does this by starting with
whatever data we've currently mined. If we want to restart, we must delete the data file.
"""

USER_LIST = "userlist_0"

import pickle
import sys

import crawler.htmlparser as parser
import crawler.userlist as userlist
from crawler.general import print_, overwrite, read
from crawler.user import User


def make_user(userid):
    """
    Make a user object, which holds information about the user along with all
    the books the user has. The books are stored as userbook objects
    :param userid: The id of the user.
    :return: a user object
    """

    try:

        soup = parser.get_soup(userid)

        print_("Parsing page...")

        # Make user object and save information
        user = User()
        user.profile_type = parser.extract_user_type(soup)
        user.number_books = parser.extract_num_books(soup)

        # Abort if user is private, empty, or non-existent
        if user.profile_type != "normal":
            return user

        # Get and save books
        books = parser.list_books(soup, userid)
        for book in books:
            userbook = user.make_userbook(book)
            user.userbooks.append(userbook)

        return user

    except:  # If cannot process user

        user = User()
        user.profile_type = "error"
        print_("Error: Cannot process user.")
        return user


def crawl_and_save(userlist_name, userlistpath="userlist_db/", load_data=True):
    """
    Crawls forever, and saves the data to the extracted data folder.
    We can stop it and it will start where it left off.
    (Though it will skip the user we were just on because it will think
    we got their data. Our data set is big enough that this should not
    be a real issue.)
    :param load_data: If true, load our previous data. Should disable for testing
    or if re-running a portion of the list.
    :param userlist_name: Name of userlist file to crawl
    :return: "Finished" if finished.
    """

    # Load data. If no file exists then start with empty list.
    try:
        if load_data:
            users = read("extracted_data/" + userlist_name + "_data")
        else:
            users = []
    except:
        users = []

    userid = None

    # Main loop
    while True:

        # Get next user. If none, then run finished function.
        userid = userlist.next_user(userlist_name, path=userlistpath)
        if userid == "finished":
            finished(users, userlist_name)

        print_("Begin extraction for user {}.".format(userid))

        # Make each user.
        user = make_user(userid)
        users.append(user)

        # Build the dataframe for the user
        user.build_dataframe()
        if user.profile_type == "normal":
            print_(user.dataframe.head(n=5))

        # Save the data.
        print_("Saving data...")
        overwrite(users, "extracted_data/" + userlist_name + "_data")
        print_("Saved. \n")


def finished(users, userlist_name):
    """
    If we finish, save the data.
    :return:
    """
    # If we somehow finish.
    overwrite(users, "extracted_data/" + userlist_name + "_data")
    print("Extraction finished! :D")

    sys.exit()


if __name__ == "__main__":
    crawl_and_save(USER_LIST)
