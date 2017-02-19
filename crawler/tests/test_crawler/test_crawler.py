"""
This tests the crawler on extracting and saving data.
This test is not automatic. We have a group of users and, by hand, go through
the information to see if it looks right.

Note that this test restarts the counter each time we run it.
"""

import crawler.main as crawler
import pickle


# 42 is private
# 7 is author
# 11 cannot be found and brings us to the homepage
# 15 cannot be found and brings us to the author page
# 2419628 Rachel
# 10815061 Taom
# 54471292 Angela
# 29320549 - says no book but has two???


def make_test_userlists(userlist):
    pickle.dump(userlist, open("test_userlist", "wb+"))
    pickle.dump(int(0), open("test_userlist_counter", "wb+"))


list = [42, 7, 11, 15, 2419628, 10815061, 54471292, 29320549]
make_test_userlists(list)

crawler.crawl_and_save("test_userlist", userlistpath="")
