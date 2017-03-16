import shelve

s = shelve.open('bookshelf.db')

print(s["total books"])
