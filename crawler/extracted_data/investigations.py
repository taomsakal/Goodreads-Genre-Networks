"Scratch file to look at extracted data"

import pickle

import pandas

data = pickle.load(open("userlist_0_data", "rb"))




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


print(data[0].dataframe)
