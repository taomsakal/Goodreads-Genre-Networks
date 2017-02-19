import pickle
import pandas

data = pickle.load(open("userlist_0_data", "rb"))


def print_full(x):
    """
    Prints the full dataframe.
    """
    pandas.set_option('display.max_rows', len(x))
    print(x)
    pandas.reset_option('display.max_rows')


def to_dataframe(data):
    """
    Puts the data in a Panda's dataframe with columns user id, book id, rating, book title
    :param data:
    :return:
    """
    userids = []
    titles = []
    ratings = []
    goodreadsids = []

    for user in data:
        userid = user[0]
        for book_info in user[1]:
            userids.append(userid)
            titles.append(book_info[0])
            goodreadsids.append(book_info[1])
            ratings.append(book_info[2])

    data = {"Title": titles, "Rating": ratings, "Goodreads ID": goodreadsids, "User Id": userids}
    dframe = pandas.DataFrame(data)

    return dframe


to_dataframe(data)
