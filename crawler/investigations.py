"Scratch file to look at extracted data"

from crawler.general import read, overwrite

data = read("extracted_data/test_data")

print(data[100].id)
