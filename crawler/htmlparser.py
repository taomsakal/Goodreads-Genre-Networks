"""
Here live all the functions that deal with getting the html of a page and parsing the information.
We import this module as parser.
"""

import math
import re
import urllib

from bs4 import BeautifulSoup

from crawler.general import print_


def get_soup(user_id, print_status=True):
    """
    Gets the html of page 1 of a user's read-bookshelf.
    :todo: We should be able to append ?per_page=100 to the end of url, but does not work.
    :param user_id: Id of user
    :return: beautifulsoup soup object
    """

    print_("Downloading Page...")

    while True:  # Determination
        try:

            # Get info from correct page
            url = 'https://www.goodreads.com/review/list/{}?shelf=read'.format(user_id)
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')

            return soup

        except:
            print_("Could not connect. Retrying...")


def extract_user_type(soup):
    """
    Extract the type of user.
    :param soup:
    :return: "normal", "private", "restricted" or "empty".
    """

    if not page_exists(soup):
        print_("User does not exist.")
        return "does not exist."
    elif is_restricted(soup):
        print_("User is restricted.")
        return "restricted"
    elif is_private(soup):
        print_("User is private.")
        return "private"
    elif extract_num_books(soup) < 1:
        print_("User is empty.")
        return "empty"
    else:
        print_("User is normal")
        return "normal"


def page_exists(soup):
    """
    Tells if the page exists.
    :param soup: soup of page
    :return: bool
    """

    # If the user does not exist we go to the home, which has specific title text.
    text = soup.title.text
    if "Share Book Recommendations With Your Friends, Join Book Clubs, Answer Trivia" in text or "Page Not Found" in text:
        return False

    return True


def is_private(soup):
    """
    Returns true if the user's profile is private.
    :param soup: soup object of page
    :return: bool
    """

    rawtext = soup.text

    if "This Profile is Private" in rawtext or "private profile" in rawtext:
        return True

    return False


def is_restricted(soup):
    """
    Returns if the profile is restricted to goodreads users
    :param soup: soup object of page
    :return: bool
    """

    rawtext = soup.text

    if "This Profile Is Restricted to Goodreads Users" in rawtext:
        return True

    return False


def list_books(soup, userid, print_status=True):
    """
    Takes in the user id and finds all that user's books, and the number of them. (W
    :param print_status: If true, print the status of the crawl
    :param soup: html of the page
    :return: list of htmlbooks
    """

    # figure out how many pages we must parse
    num_books = extract_num_books(soup)
    pages_to_parse = math.ceil(num_books / 30)

    # if empty user
    if num_books < 1:
        return "Empty User"

    # Parse the pages
    books = []
    for i in range(0, pages_to_parse):
        print_("Extracting books for user {}. Page {}/{}".format(userid, i + 1, pages_to_parse))

        # Extract books from current page
        books += extract_books(soup, i, userid)

    return books


def extract_title(htmlbook):
    """
    Gets the title of a book.
    :param htmlbook: html data for single book.
    :return: Title as a string
    """

    rawtext = htmlbook.find("td", class_="field title").text

    text = rawtext.splitlines()[1]

    text = text.strip()

    return text


def extract_books(soup, page_number, userid):
    """
    Gets the of the books in each page.
    Can also just return the source code of the page instead.
    :param return_soup: If true, return page code instead of list of books code
    :param soup: soup of the page
    :return: resultset of books
    """

    # If we are on the first page, we already have the soup information. No need to extract again.
    if page_number == 1:
        books = soup.find_all("tr", class_="bookalike review")
        return books

    # Get books from aditional pages
    while True:  # Never give up. Stay determined.
        try:

            url = 'https://www.goodreads.com/review/list/{}?page={}&shelf=read'.format(userid, page_number + 1)
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')

            books = soup.find_all("tr", class_="bookalike review")
            break

        except:  # Happens if there are connection problems

            print_("Cannot connect. Retrying...")

    return books


def extract_num_books(soup):
    """
    Extracts the number of books in the shelf.
    :param soup: html soup of all bookshelf
    :return: The number of books, or None if failed
    """

    text = soup.find('title').text
    if "of 0" in text:
        return 0

    # There are at least two ways to display the number of books in the page.
    try:
        try:
            num = re.findall(r'of (.*?)\)', text)  # extract the number
            num = int(num[0].replace(",", ""))
        except:
            num = re.findall(r'\((.*?) books\)', text)  # extract the number
            num = int(num[0].replace(",", ""))
    except:
        raise Exception("Cannot extract number of books")

    return num


def extract_username(soup):
    """
    Extracts username of a user
    :param soup: html soup of bookshelf
    :return: The number of books
    """

    text = soup.find('title').text

    try:
        username = re.findall(r'| (.*?)\)\'s bookshelf', text)
    except:
        username = "Cannot extract username"

    return username

def extract_link(htmlbook):
    """
    Extract part of a link to the book.
    The link will have the goodreads id number.
    :param htmlbook: html data for single book.
    :return: A link string
    """

    return htmlbook.find('a', href=True)['href']


def extract_goodreads_id(htmlbook):
    """
    Gets the goodreads id of a book.
    :param htmlbook: html data for single book.
    :return: Goodreads id
    """

    link = extract_link(htmlbook)

    # Extract the number from the link
    link = link[11:]  # remove '/book/show/' from start
    link = link.split('.', 1)[0]  # remove everything after the dot
    link = link.split('-', 1)[0]  # remove everything after the -

    return int(link)


def extract_user_rating(htmlbook):
    """
    Gets the user rating of the book
    :param htmlbook: html data for single book.
    :return: integer from 0 to 5
    """

    rawtext = htmlbook.find("td", class_="field rating").text

    rating = rawtext.splitlines()[1]

    if rating == "it was amazing":
        return 5
    elif rating == "really liked it":
        return 4
    elif rating == "liked it":
        return 3
    elif rating == "it was ok":
        return 2
    elif rating == "did not like it":
        return 1
    else:
        return 0


def extract_read_count(htmlbook):
    """
    Extract the number of times the book has been read.
    :param htmlbook: html for the book
    :return: number of times book has been read
    """
    rawtext = htmlbook.find("td", class_="field read_count").text

    # Process the text into an integer
    text = rawtext.replace("# times read", "")
    text = text.strip()

    try:
        return int(text.replace(",", ""))
    except:  # May have a read count such as "2+"
        return text


def extract_date_added(htmlbook):
    rawtext = htmlbook.find("td", class_="field date_added").text

    # Process the text into an integer
    text = rawtext.replace("date added", "")
    text = text.strip()

    return text


def extract_date_purchased(htmlbook):
    rawtext = htmlbook.find("td", class_="field date_purchased").text

    # Process the text into an integer
    text = rawtext.replace("date purchased", "")
    text = text.strip()

    return text


def extract_owned(htmlbook):
    rawtext = htmlbook.find("td", class_="field owned").text

    # Process the text into an integer
    text = rawtext.replace("owned", "")
    text = text.strip()

    if text != "":
        print(rawtext)
        print(text)

    return text


def extract_purchase_location(htmlbook):
    rawtext = htmlbook.find("td", class_="field purchase_location").text

    text = rawtext.replace("purchase location", "")
    text = text.strip()

    if text != "":
        print(rawtext)
        print(text)

    return text


def extract_book_condition(htmlbook):
    rawtext = htmlbook.find("td", class_="field condition").text

    text = rawtext.replace("condition", "")
    text = text.strip()

    if text != "":
        print(rawtext)
        print(text)

    return text


def extract_book_format(htmlbook):
    """
    Extract the books format
    :param htmlbook: html of the book
    :return: name of the format
    """
    rawtext = htmlbook.find("td", class_="field format").text

    # Process the text into an integer
    text = rawtext.replace("format", "")
    text = text.strip()

    return text


def extract_review(htmlbook):
    """
    Extracts a snippet if a review for the book
    :param htmlbook: html of the book
    :return: review
    """
    rawtext = htmlbook.find("td", class_="field review").text

    text = rawtext.splitlines()[1:]
    text = "\n".join(text)
    text = text.strip()

    return text


def extract_recommender(htmlbook):
    """
    Extract the user that recommended the book?
    :param htmlbook: html of a book
    :return: username of recommender
    """
    rawtext = htmlbook.find("td", class_="field recommender").text

    text = rawtext[11:]  # Cut out first part, w/o risking cutting out a user named "reccommender"

    return text


def extract_notes(htmlbook):
    """
    Extracts the notes. These are private so kinda useless?
    :param htmlbook: html of a book
    :return: notes, or text saying notes are private
    """
    rawtext = htmlbook.find("td", class_="field notes").text

    text = rawtext.replace("notes", "")
    text = text.strip()

    return text


def extract_comments(htmlbook):
    """
    Extracts the number of comments.
    # Todo: figure out what comments are.
    :param htmlbook: html of a book
    :return: The number of comments
    """
    rawtext = htmlbook.find("td", class_="field comments").text

    # Process the text into an integer
    text = rawtext.replace("comments", "")
    text = text.strip()

    return int(text.replace(",", ""))


def extract_votes(htmlbook):
    """
    Extract the number of votes. (votes on what?)
    :param htmlbook: html of a book
    :return: number of votes
    """
    rawtext = htmlbook.find("td", class_="field votes").text

    # Process the text into an integer
    text = rawtext.replace("votes", "")
    text = text.strip()

    return int(text.replace(",", ""))


def extract_date_pub_edition(htmlbook):
    """
    Extracts the date published
    :param htmlbook: html of a book
    :return: a date
    """
    rawtext = htmlbook.find("td", class_="field date_pub_edition").text

    # Process the text into an integer
    text = rawtext.replace("date pub edition", "")
    text = text.strip()

    return text

# All the data below we can extract from the goodreads book object, so we do not bother with it.

# def extract_author(htmlbook):
#     """
#     Gets the author of a book.
#     :param htmlbook: html data for single book.
#     :return: Author name
#     """
#
#     rawtext = htmlbook.find("td", class_="field author").text
#
#     return rawtext
#
# def extract_isbn(htmlbook):
#     """
#     Gets a book's isbn number.
#     :param htmlbook: html data for single book.
#     :return: isbn integer
#     """
#
#     rawtext = htmlbook.find("td", class_="field isbn").text
#
#     return rawtext # todo return as int
#
# def extract_isbn13(htmlbook):
#     """
#     Gets the isbn13 number of a book.
#     :param htmlbook: html data for single book.
#     :return: isbn13 integer
#     """
#
#     rawtext = htmlbook.find("td", class_="field isbn13").text
#
#     return rawtext # todo return as int
#
# def extract_asin(htmlbook):
#     """
#     Gets the asin (Amazon standard id number) of a book.
#     :param htmlbook: html data for single book.
#     :return: asin as integer
#     """
#
#     rawtext = htmlbook.find("td", class_="field asin").text
#
#     return rawtext
#
# def extract_num_pages(htmlbook):
#     """
#     Gets the number of pages in a book.
#     :param htmlbook: html data for single book.
#     :return: number of pages
#     """
#
#     rawtext = htmlbook.find("td", class_="field num_pages").text
#
#     return rawtext
#
# def extract_avg_rating(htmlbook):
#     """
#     Gets the average rating of a book.
#     :param htmlbook: html data for single book.
#     :return: average rating
#     """
#
#     rawtext = htmlbook.find("td", class_="field avg_rating").text
#
#     return rawtext



# b = books[0].find_all("td", class_="field num_ratings")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field date_pub")
# print(b)
#
# print("----------")
#

#
