import shelve
import pandas
import os
from crawler.general import read
from matplotlib import pyplot as plot
from crawler.amazonbook import AmazonBook
import pandas
from goodreads.book import GoodreadsBook

def genre_statistics(show_progress=True, save_results=True):
    """
    :return: A dataframe with the overall number of each genre.
    """

    d = {}
    amazon_books = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')

    l = len(amazon_books)
    i = 0

    # Make dictionary with number of books in each genre.
    for key, book in amazon_books.items():
        if show_progress:
            i += 1
            print_progress("Calculating Genre Distribution", i, l, 1000)
        if isinstance(book, AmazonBook):
            genres = set(book.genres)  # Remove repeats of genres by turning list into set
            for genre in genres:
                if genre in d:
                    d[genre] += 1
                else:
                    d[genre] = 1

    # Make data into a dataframe and save it.
    genre_data = pandas.DataFrame(list(d.items()), columns=['Genre', 'Number of Books'])
    if save_results:
        genre_data.to_csv("results/genre_distribution.csv")

    return genre_data

def language_stats(show_progress=True, save_results=True):
    """
    :return: A datafram with the overall number of each language.
    """

    d = {}
    amazon_books = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')

    l = len(amazon_books)
    i = 0

    # Make dictionary with number of books in each genre.
    for key, book in amazon_books.items():
        if show_progress:
            i += 1
            print_progress("Calculating Language Distribution", i, l, 1000)
        if isinstance(book, AmazonBook):
            languages = set(book.languages)  # Remove repeats of genres by turning list into set
            for languages in languages:
                if languages in d:
                    d[languages] += 1
                else:
                    d[languages] = 1

    # Make data into a dataframe and save it.
    genre_data = pandas.DataFrame(list(d.items()), columns=['Language', 'Number of Books'])
    if save_results:
        genre_data.to_csv("results/language_distribution.csv")

    return genre_data

def user_book_num(show_progress=True, save_results=True):
    """
    :return: A dataframe with number of books and number of users with that number of books.
    """

    d = {}
    l = len(os.listdir("../data/userlists"))
    i = 0

    for filename in os.listdir("../data/userlists"):

        if show_progress:
            i += 1
            print_progress("Calculating book number distribution.", i, l, 1)

        userlist = read("../data/userlists/" + filename)
        for user in userlist:
            if user.profile_type == "normal":
                book_num = str(len(user.userbooks))
                if book_num in d:
                    d[book_num] += 1
                else:
                    d[book_num] = 1

    # Make data into a dataframe and save it.
    genre_data = pandas.DataFrame(list(d.items()), columns=['Book Number', 'Number of Users'])
    if save_results:
        genre_data.to_csv("results/user_book_number_distribution.csv")

    return genre_data


def book_read_number(show_progress=True, save_results=True):
    """
    :return: A dataframe with book id and number of times that book has been read.
    """

    # Init counter
    l = len(os.listdir("../data/userlists"))
    i = 0
    d = {}

    for filename in os.listdir("../data/userlists"):

        if show_progress:
            i += 1
            print_progress("Calculating book reader number distribution.", i, l, 1)

        userlist = read("../data/userlists/" + filename)
        for user in userlist:
            if user.profile_type == "normal":
                for book in user.userbooks:
                    if str(book.goodreads_id) in d:
                        d[str(book.goodreads_id)] += 1
                    else:
                        d[str(book.goodreads_id)] = 1

    # Make data into a dataframe and save it.
    data = pandas.DataFrame(list(d.items()), columns=['Book ID', 'Number Readers'])
    if save_results:
        data.to_csv("results/book_reader_number_distribution.csv")

    return data

def user_book_dataframe(show_progress=True, save_results=True):
    """
    :return: A dataframe with book id and number of times that book has been read.
    """

    goodreads_books = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')
    data_list = []

    # Init counter
    l = len(os.listdir("../data/userlists"))
    i = 0

    for filename in os.listdir("../data/userlists"):

        if show_progress:
            i += 1
            print_progress("Calculating book reader number distribution.", i, l, 1)

        userlist = read("../data/userlists/" + filename)
        for user in userlist:
            if user.profile_type == "normal":
                for book in user.userbooks:
                        d = {}
                        d["Goodreads ID"] = book.goodreads_id
                        d["Title"] = goodreads_books[str(book.goodreads_id)]
                        # d[] = book.goodreads_id = "No gid"
                        #
                        # d[] = book.rating = "No rating"
                        # d[] = book.readcount = 0
                        #
                        # d[] = book.date_added = "No added date"
                        # d[] = book.date_purchased = "No purchase date"
                        # d[] = book.owned = "No owned info"
                        # d[] = book.purchase_location = None
                        # d[] = book.condition = None
                        # d[] = book.format = None
                        # d[] = book.review = None
                        # d[] = book.recomender = None
                        # d[] = book.notes = None
                        # d[] = book.comments = None
                        # d[] = book.votes = None
                        # d[] = book.date_pub_edition = None
                        # d[] = book.link = None



    # Make data into a dataframe and save it.
    data = pandas.DataFrame(list(d.items()), columns=['Book ID', 'Number Readers'])
    if save_results:
        data.to_csv("results/userbook_dataframe.csv")

    return data



def goodreads_book_dataframe(show_progress=True, save_results=True):
    """
    Make a csv and data frame for the goodreads books.
    :return: 
    """

    goodreads_books = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')
    data_list = []

    # Init counter
    l = len(os.listdir("../data/userlists"))
    i = 0

    for filename in os.listdir("../data/userlists"):

        if show_progress:
            i += 1
            print_progress("Building Goodreads Dataframe", i, l, 1)

        for book in goodreads_books:
            d = {}
            d["Goodreads ID"] = book.goodreads_id
            d["Title"] = book.title
            d["Authors"] = book.authors
            d["Description"] = book.description
            d["Average Rating"] = book.average_rating
            d["Rating Distribution"] = book.rating_dist
            d["Ratings Count"] = book.ratings_count
            d["Text Reviews Count"] = book.text_reviews_count
            d["Num Pages"] = book.num_pages
            d["Popular Shelves"] = book.popular_shelves
            d["Work"] = book.work
            d["Series Works"] = book.series_works
            d["Publication Date"] = book.publication_dat
            d["Publisher"] = book.publisher
            d["Language"] = book.language_code
            d["Edition Info"] = book.edition_information
            d["Image URL"] = book.image_url
            d["Small Image URL"] = book.small_image_url
            d["Is Ebook"] = book.is_ebook
            d["Format"] = book.format
            d["ISBN"] = book.isbn


def print_progress(text, current, total, step):
    """
    Prints the current progress ever step iterations.
    """

    percent = current / total * 100
    percent = int(percent)

    if current % step == 0:

        print("{}: {}/{} ({}%)".format(text, current, total, percent))

def user_profile_statistics():
    """
    This gets the counts of user types.
    :return: 
    """

    total_users = 0
    normal_users = 0
    private_users = 0
    empty_users = 0
    error_users = 0
    no_type_users = 0
    users_with_no_id = 0


    for filename in os.listdir("../data/userlists"):

        print("Processing {}".format(filename))
        userlist = read("../data/userlists/" + filename)

        for user in userlist:
            total_users += 1
            if user.profile_type == "normal":
                normal_users += 1
            elif user.profile_type == "private":
                private_users += 1
            elif user.profile_type == "empty":
                empty_users += 1
            elif user.profile_type == "error":
                error_users += 1
            elif user.profile_type == "no type":
                no_type_users += 1

            if user.id == 0:
                users_with_no_id += 1

    print("Total Users: {}".format(total_users))
    print("Normal Users: {}".format(normal_users))
    print("Private Users: {}".format(private_users))
    print("Empty Users: {}".format(empty_users))
    print("Error Users: {}".format(error_users))
    print("No Type Users: {}".format(no_type_users))
    print("No ID Users: {}".format(users_with_no_id))


if __name__ == "__main__":

    user_profile_statistics()
    # genre_statistics()
    #language_stats()
    # user_book_num()
    # book_read_number()





