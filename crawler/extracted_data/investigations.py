"Scratch file to look at extracted data"

from crawler.general import read

data = read("userlist_0_data")

print(data[-1].dataframe)
print("--------")
print("Number of users: " + str(len(data)))
