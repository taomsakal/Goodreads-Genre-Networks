import shelve
from crawler.amazonbook import AmazonBook

s = shelve.open('amazon_bookshelf.db', flag="r")

print(len(s))


# for k in s.values():
#     if isinstance(k, AmazonBook):
#         print(k.sales_rank)
#         print(k.genres)
#         print(k.asin)
#         print(k.languages)
#         print(k.nodes)
#         print(k.reviews)
#         print("-"*30 + "\n")
