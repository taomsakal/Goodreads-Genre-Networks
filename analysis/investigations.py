"Scratch file to look at extracted data"

import os
from crawler.general import read, overwrite
import shelve
import pickle




#amazon_books = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')
#
# print(amazon_books)
#
# for key, value in amazon_books.items():
#     print(value.languages)
goodreads_books = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')
amazon_books = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')
print(type(goodreads_books.values()))
print(type(amazon_books.values()))
print(goodreads_books["1"].gid)
print(amazon_books["1"].genres)
# for key, value in amazon_books.items():
#     print(key, value)
#     print(type(value))
#     print(dir(value))