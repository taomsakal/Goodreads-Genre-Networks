"Scratch file to look at extracted data"

from crawler.general import read, overwrite

data = read("userlist_0_data_1")

print(data[-1].dataframe)
print("--------")
print("Number of users: " + str(len(data)))
print(len(data[-1].dataframe))

data1 = data[0:5000]
data2 = data[5000:10000]

overwrite(data1, "userlist_0_data_1_1")
overwrite(data2, "userlist_0_data_1_2")
