import shelve
from goodreads.book import GoodreadsBook
from crawler.amazonbook import AmazonBook

# Source
amazonbs = 'amazon_bookshelf.db'
goodreadsbs = 'bookshelf.db'

# Targets
new_goodreads = 'goodreads_bookshelf.db'
new_amazon = 'new_amazon_bookshelve.db'


def clean_bookshelf(source, target, obj_type):
    """
    Copies a bookshelf source to the target bookshelf. We only copy valid entries
    of gid: book_obj where the book_obj is of obj_type
    :param source: Source bookshelf
    :param target: Target bookshelf
    :return: None
    """

    source = shelve.open(source, flag='r')
    target = shelve.open(target)

    length = len(source)
    i = 0
    for key in source.keys():
        if isinstance(source[key], obj_type):
            target[key] = source[key]
            i += 1

            print(source[key])
            print("{}/{}\n".format(i, length))

    source.close()
    target.close()


if __name__ == '__main__':
    clean_bookshelf(amazonbs, new_amazon, AmazonBook)
