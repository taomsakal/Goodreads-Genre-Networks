"""
This tests the crawler on extracting and saving data.
This test is not automatic. We have a group of users and, by hand, go through
the information to see if it looks right.

Note that this test restarts the counter each time we run it.
"""

import crawler.bookworm as crawler
from crawler.general import overwrite


def make_test_userlists(userlist):
    overwrite(userlist, "test_userlist")
    overwrite(int(0), "test_userlist_counter")


# 7 is author
# 11 cannot be found and brings us to the homepage
# 15 cannot be found and brings us to the author page
# 42 is private
# 60 cannot be found and brings us to the homepage
# 2419628 Rachel (aka The Champion)
# 10815061 Taom
# 54471292 Angela
# 29320549 - says no book but has two???
# 6693775 - restricted to goodreads users
# 3146916 - another version of private profile
# 19218152 - had an error for some reason
# 64405638 - strange num books
# 61021479 - strange num books
# 62149778 - different page not found
# 765173 - defeated Rachel in page number but disqualified because two people.

userids = [11, 42, 7, 19218152, 64405638, 61021479, 15, 62149778, 2419628, 10815061, 54471292, 29320549, 6693775,
           3146916]
make_test_userlists(userids)

crawler.crawl_and_save("test_userlist", userlistpath="", load_data=False)
