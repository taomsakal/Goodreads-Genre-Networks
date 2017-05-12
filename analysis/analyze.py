import shelve
import sys

sys.path.append("../")
from crawler.general import *
from crawler.amazonbook import AmazonBook
from amazon.api import AmazonAPI
import pickle
from collections import Counter

s = shelve.open('../data/book_db/amazon_bookshelf.db')

with open('clusters.pickle', 'rb') as f:
    clusters = pickle.load(f)

genre_clusters = {c: [] for c in clusters}
for c in clusters:
    book_list = clusters[c]
    for book_info in book_list:
        goodreads_id = book_info.split("__")[1]  # string
        if goodreads_id in s and s[goodreads_id] != "Skipped":
            genre_clusters[c].extend(s[goodreads_id].genres)

genre_distribution = {c: Counter(genre_clusters[c]) for c in genre_clusters}

with open('genre_distribution.pickle', 'wb') as f:
    pickle.dump(genre_distribution, f, protocol=2)
