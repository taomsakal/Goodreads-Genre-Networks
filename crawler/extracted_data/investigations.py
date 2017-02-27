"Scratch file to look at extracted data"

import pickle


data = pickle.load(open("userlist_0_data", "rb"))

print(data[1001].dataframe)
print("--------")
print("Number of users: " + str(len(data)))
