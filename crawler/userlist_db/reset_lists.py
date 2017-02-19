"""
This will create the userlist database where it is run.
WARNING: Will overwrite old databases and counters
"""

import crawler.userlist as ul

print("Creating userlist database... (This may take a few minutes)")
ul.make_userlist_database("userlist", ul.GOODREADS_SIZE, 15)
print("Finished!")
