"""
Running this makes/resets the lists. Be careful not to overwrite the existing lists.
This will also take a while beacuse it works with ~65mil users.
"""

import crawler.userlist as ul

ul.make_and_save_list(10, "userlist")
