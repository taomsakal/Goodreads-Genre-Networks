"Scratch file to look at extracted data"

import os
from crawler.general import read, overwrite
import shelve

#amazon_books = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')
#
# print(amazon_books)
#
# for key, value in amazon_books.items():
#     print(value.languages)
goodreads_books = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')
for filename in os.listdir("../data/userlists"):
    userlist = read("../data/userlists/" + filename)
    for user in userlist:
        if user.profile_type == "normal":
            for book in user.userbooks:
                print(book.rating)
                print(goodreads_books[str(book.goodreads_id).title()])