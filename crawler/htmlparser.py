from goodreads import client
from bs4 import BeautifulSoup
import urllib
import time
import re
import math


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


def list_books(user_id, print_status=True):
    """
    Takes in the user id and finds all that user's books, and the number of them. (We get this num for later stats.)
    Can also output error messeges.
    :param print_status: If true, print the status of the crawl
    :param user_id: The user id
    :return: (booklist, book number) or ("Page does not exist", None) or ("Profile is private", book number)
    """

    if print_status:
        print("Begin extraction for user {}".format(user_id))

    # Get info from correct page
    if print_status:
        print("Connecting...")

    url = 'https://www.goodreads.com/review/list/{}?shelf=read'.format(user_id)
    # We should be able to append ?per_page=100 to the end of this,
    # but even if we do it gives back only 30 books. This does not happen in chrome.

    if print_status:
        print("Connected!".format(user_id))
        print("Parsing Page...")

    soup = extract_books(url, return_soup=True)  # Get the entire page

    if not page_exists(soup):
        return "Page does not exist", None

    # figure out how many pages we must parse
    num_books, private = extract_num_books(soup)
    pages_to_parse = math.ceil(num_books / 30)

    # if empty user
    if num_books < 1:
        return "Empty User", num_books

    # If profile is not private, then crawl it.
    if not private:
        books = soup.find_all("tr", class_="bookalike review")  # Gives list of books with info

        # Parse the remaining pages
        for i in range(0, pages_to_parse):

            if print_status:
                print("Extracting books for user {}. Page {}/{}".format(user_id, i + 1, pages_to_parse))

            url = 'https://www.goodreads.com/review/list/{}?page={}&shelf=read'.format(user_id, i + 1)
            books += extract_books(url)

        return books, num_books

    return "Profile is private", num_books


def extract_books(url, return_soup=False):
    """
    Gets the of the books in each page.
    Can also just return the source code of the page instead.
    :param return_soup: If true, return page code instead of list of books code
    :param url: url of page
    :return: resultset of books
    """

    while True:  # Never give up. Stay determined.
        try:
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')
            books = soup.find_all("tr", class_="bookalike review")
            break
        except TimeoutError:
            pass

    if not return_soup:
        return books
    else:
        return soup


def page_exists(html):
    """
    Tells if the page exists.
    :param html: html of page
    :return: bool
    """

    # If the user does not exist we go to the home page or the author page.
    # We can look at the title to learn if we went to one.

    text = html.find('title').text
    if "Goodreads | Recent Updates" in text or "Goodreads Authors" in text:
        return False
    else:
        return True


def extract_num_books(html):
    """
    Extracts the number of books in the shelf and if the profile is private.
    This tells us how many pages we must crawl to see all books.
    :param html: html soup of all bookshelf
    :return: The number of books
    """

    text = html.find('title').text

    try:
        num = re.findall(r'of (.*?)\)', text)  # extract the number
        num = int(num[0].replace(",", ""))
        private = False
    except:  # if private
        num = re.findall(r'\((.*?) books\)', text)  # extract the number
        num = int(num[0].replace(",", ""))
        private = True

    return num, private


def extract_username(html):
    """
    Extracts username of a user
    :param html: html soup of bookshelf
    :return: The number of books
    """

    text = html.find('title').text

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
    rawtext = htmlbook.find("td", class_="field read_count")
    num = rawtext.splitlines()[1]

    return num


def extract_date_added(htmlbook):
    rawtext = htmlbook.find("td", class_="field date_added")
    date = rawtext.splitlines()[1]

    return date


def extract_date_purchased(htmlbook):
    rawtext = htmlbook.find("td", class_="field date_purchased")
    date = rawtext.splitlines()[1]

    return date


def extract_owned(htmlbook):
    """
    Extracts... something to do about if the user owns the book.
    :param htmlbook:
    :return:
    """
    rawtext = htmlbook.find("td", class_="field owned")
    data = rawtext.splitlines()[1]

    return data


def extract_purchase_location(htmlbook):
    rawtext = htmlbook.find("td", class_="field purchase_location")
    data = rawtext.splitlines()[1]

    return data


def extract_book_condition(htmlbook):
    rawtext = htmlbook.find("td", class_="field condition")
    data = rawtext.splitlines()[1]

    return data


def extract_book_format(htmlbook):
    rawtext = htmlbook.find("td", class_="field format")
    data = rawtext.splitlines()[1]

    return data


def extract_review(htmlbook):
    rawtext = htmlbook.find("td", class_="field review")
    data = rawtext.splitlines()[1]

    return data


def extract_recommender(htmlbook):
    rawtext = htmlbook.find("td", class_="field recommender")
    data = rawtext.splitlines()[1]

    return data


def extract_notes(htmlbook):
    rawtext = htmlbook.find("td", class_="field notes")
    data = rawtext.splitlines()[1]

    return data


def extract_comments(htmlbook):
    rawtext = htmlbook.find("td", class_="field comments")
    data = rawtext.splitlines()[1]

    return data


def extract_votes(htmlbook):
    rawtext = htmlbook.find("td", class_="field votes")
    data = rawtext.splitlines()[1]

    return data


def extract_date_pub_edition(htmlbook):
    rawtext = htmlbook.find("td", class_="field date_pub_edition")
    data = rawtext.splitlines()[1]

    return data

# All the data below we can extract from the goodreads book object

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
