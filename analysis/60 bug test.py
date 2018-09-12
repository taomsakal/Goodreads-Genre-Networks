import csv
import os

import seaborn as sb

from analysis.overall_statistics import print_progress
from crawler.general import *


def output_users_with_n_books(n, show_progress=True, save_results=True):
    """
    Outputs the ids of the users with exactly n books. For debugging the 60 book data point.
    :param n:
    :param show_progress:
    :param save_results:
    :return:
    """

    l = len(os.listdir("../data/userlists"))
    i = 0
    idlist = []

    for filename in os.listdir("../data/userlists")[0:10]:

        if show_progress:
            i += 1
            print_progress("Calculating book number distribution.", i, l, 1)

        userlist = read("../data/userlists/" + filename)
        for user in userlist:
            if user.profile_type == "normal":
                book_num = len(user.userbooks)
                if book_num == n:
                    # print(user.id, user.number_books, len(user.userbooks), user.name, user.profile_type, [userbook.goodreads_id for userbook in user.userbooks])
                    # print([userbook.goodreads_id for userbook in user.userbooks], ',')
                    idlist.append([user.id, user.number_books, [userbook.goodreads_id for userbook in user.userbooks]])

    return idlist


# l = output_users_with_n_books(60)
# for user in l:
#     print(f"Length of list: {len(user[2])} \nNumber of duplicates: {len(set(user[2]))} \nTrue number: {user[1]}")

# Find the number of users with the same number of books as userbook list

def find_true_books():
    l = len(os.listdir("../data/userlists"))
    i = 0
    num_correct = 0
    num_incorrect = 0
    incorrect_list = []
    correct_list = []

    for filename in os.listdir("../data/userlists")[0:]:

        i += 1
        print_progress("Calculating book number distribution.", i, l, 1)

        userlist = read("../data/userlists/" + filename)
        for user in userlist:
            if user.profile_type == "normal":
                gid_list = [userbook.goodreads_id for userbook in user.userbooks]
                book_num = len(gid_list)
                unique_num = len(set(gid_list))
                true_num = user.number_books
                no_id_count = len([i for i in gid_list if i == "No gid"])  # Set will have some dups because of no gids

                print(book_num, unique_num, true_num, no_id_count)

                if true_num == unique_num:
                    num_correct += 1
                    correct_list.append((book_num, unique_num, true_num, no_id_count, user.id))
                else:
                    num_incorrect += 1
                    incorrect_list.append((book_num, unique_num, true_num, no_id_count, user.id))

    print(num_correct, num_incorrect, num_correct / (num_correct + num_incorrect))

    incorrect_length = len(incorrect_list)

    book_num_list = []
    unique_num_list = []
    true_num_list = []
    for i in incorrect_list:
        book_num_list.append(i[0])
        unique_num_list.append(i[1])
        true_num_list.append(i[2])
        print(
            f"Averages\n book num: {sum(book_num_list)/incorrect_length}\n unique num: {sum(unique_num_list)/incorrect_length}\ntrue num: {sum(true_num_list)/incorrect_length}")

    make_csv(correct_list, "correct_list")
    make_csv(incorrect_list, "incorrect_list")
    make_csv(correct_list + incorrect_list, "both_list")

    return incorrect_list


def make_csv(l, name):
    """
    Makes a csv of the list
    :param l:
    :return:
    """

    with open(f'{name}.csv', 'w', newline='') as file:
        wr = csv.writer(file)
        wr.writerow(["book_num", "unique_num", "true_num", "no_id_count", "user_id"])
        for i in l:
            wr.writerow(list(i))


def clean_inconsistent_data(only_add_with_id=False, add_all=False):
    """

    :param only_add_with_id:
    :param add_all: Adds all normal or empty data without doing any of the checks.
    :return:
    """
    l = len(os.listdir("../data/userlists"))
    i = 0
    cleaned_userlist = []
    total_users = 0
    total_normal_users = 0
    total_errors = 0

    for filename in os.listdir("../data/userlists"):

        i += 1
        print_progress("Cleaning the userlist data.", i, l, 1)

        userlist = read("../data/userlists/" + filename)
        for user in userlist:
            total_users += 1
            if user.profile_type == "normal" or user.profile_type == "empty":
                total_normal_users += 1
                gid_list = [userbook.goodreads_id for userbook in user.userbooks]
                book_num = len(gid_list)
                unique_num = len(set(gid_list))
                true_num = user.number_books
                no_id_count = len([i for i in gid_list if i == "No gid"])  # Set will have some dups because of no gids

                if (true_num == book_num == unique_num) or add_all:  #if all data is consistant
                    if only_add_with_id: # if only want those with ids
                        if user.id != 0:
                            cleaned_userlist.append(user)
                        else:
                            total_errors += 1
                    else:
                        cleaned_userlist.append(user)
                        # print(book_num, unique_num, true_num)
                else:
                    total_errors += 1
                    if user.id != 0:
                        print(user.id, book_num, unique_num, true_num, "ERROR")
                        print([book.goodreads_id for book in user.userbooks])
                        print("")

    print(
        f"Total Users: {total_users}\nTotal Normal/empty Users: {total_normal_users}\nTotal Errors: {total_errors} "
        f"\nProportion of normal/empty out of total: {total_normal_users/total_users}"
        f"\nProportion Errors out of normal/empty: {total_errors/total_normal_users}")

    print("saving the userlist...")
    overwrite(cleaned_userlist, 'og_userlist.pickle')
    print("Userlist saved! :D")

    return cleaned_userlist

def remove_less_than(file, n):
    """
    Remove users with less than n books
    :param n:
    :return:
    """

    #file = input("What is the <filename> to read?")

    print("Reading the file...")
    userlist = read(f"{file}.pickle")

    #n = int(input("Remove users with less than <how many> books in their booklist?"))

    newlist = []

    total_users = len(userlist)
    i = 0
    for user in userlist:
        i += 1
        print_progress(f"Removing users with less than {n} books", i, total_users, 10000)
        if len(user.userbooks) >= n:
            newlist.append(user)

    print("saving file...")
    overwrite(newlist, f"{file}_geq{n}.pickle")





if __name__ == "__main__":
   clean_inconsistent_data(only_add_with_id=True, add_all=False)
   #  remove_less_than("cleaned_userlist", 1)
   #  remove_less_than("cleaned_userlist", 5)
   # remove_less_than("cleaned_userlist_with_ids", 2)



