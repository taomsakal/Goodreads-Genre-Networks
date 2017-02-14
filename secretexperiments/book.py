import re

s = " <title>odawg Diggity's  \n bookshelf: all (showing 1-30 of 110329293)(sorted by: date added)"

print(re.findall(r'of (.*?)\)', s))
