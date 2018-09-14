import os
import random
import shutil
import sys
import logging

"""
This downloads the user data and user rating data from Goodreads through their api.
It takes a random sample of users form 0 to NUM_USERS

You'll need a developer key to get any data, and permission from Goodreads to store, analyse, and publish the data.
(Please see the Goodreads API terms of use.)


"""

SPEED_LIMIT = 2  # How many seconds to wait before next request. Must be greater than one.
KEY = ''  # The developer key. You'll want to keep this secret.
NUM_USERS = 86775903  # The current number of users on Goodreads. This is accurate to within 1000 as of 9/13/2018


def make_user_list(list_size, start_number=1, end_number = NUM_USERS):
    """
    Makes a list of random users.

    Args:
        list_size: The size the list should be.
        start_number: The lower bound of sample space
        max_number: The upper bound of sample space

    Warnings:
        This is a random algorithm that takes a random number, puts them into a set of users, and once the set gets
        big enough turn the set into a list and write it.

        It'll be really slow unless list_size is much smaller than the number of users. This should generally be
        the case since there are 86 million Goodreads users

    Returns:
        A list
    """

    assert list_size >= 0

    user_set = set()

    logging.info("Creating the user list")

    # if end_number - start_number < list_size:
    #     logging.critical(f"Trying to make a list of {list_size} unique elements when there are only {end_number - start_number} of them.")
    #     raise ValueError("Not enough elements in list")
    if end_number <= start_number:
        raise ValueError("End number cannot be below or equal to start number")

    while len(user_set) < list_size:
        user_id = random.randint(start_number, end_number)
        user_set.add(user_id)

    user_list = list(user_set)

    assert len(user_set) == len(user_list)  # Make sure no duplicates got in

    return user_list

def ready_new_batch(max_num, batch_name):
    """
    Set up a folder for a new batch of users to be crawled.
    The folder will be located in data/raw/users/<folder name> and it will have three things

    1. A subfolder called "user_ratings_xml" which stores the raw user book list xml files
    2. A subfolder called "users_xml" which stores the raw user information xml files
    3. A list of random users, called "userlist.txt"
    4. A plaintext object called "current_user.txt" that tells us the current user we are on
    5. A plaintext of failed users called "failed_users.txt"
    6. A plaintext of users with questionable data called "questionable_users.txt"

    Args:
        max_num: Make number of users to download
        batch_name: Name of the batch folder

    Returns: None

    """

    # Check to make sure data doesn't already exist. If it does offer to delete.
    path = f"data/raw/users/{batch_name}"
    if os.path.exists(path):
        good_to_go = False
        logging.warning("Trying to make new batch but it already exists.")
        text = input("The batch already exists. Delete it? (y/n)")
        if text == "y":
            text = input("Are you sure? (y/n)")
            if text == "y":
                logging.warning(f"Deleting and remaking {path}")
                shutil.rmtree(path)
                good_to_go = True
    else:
        good_to_go = True

    # Make the directories
    if good_to_go:
        if not os.path.exists(path):
            logging.info("Setting up new batch...")
            os.makedirs(f"{path}/user_ratings_xml")
            os.makedirs(f"{path}/users_xml")
            save_list_as_text(f"{path}/user_id_list.txt", ["no users currently"])
            save_list_as_text(f"{path}/current_user.txt", ["no users currently"])
            save_list_as_text(f"{path}/failed_users.txt", ["no users currently"])
            save_list_as_text(f"{path}/questionable_users.txt", ["no users currently"])
            logging.info("Finished setting up new batch files")
            user_id_list = make_user_list()
        else:
            logging.critical(f"The directory {path} already exists. Aborting...")
            raise FileExistsError(f"The directory {path} already exists.")
    else:
        logging.critical("For some reason we are not good to go to set up a new batch. Aborting.")
        raise Exception("Not good to go. Unknown error")


def next_in_list(list_, txtcounter, increment_counter=False):
    """
    Reads the next line in a txt list.
    Args:
        list_: the given list
        txtcounter: the path to the counter
        increment_counter: if true then increment the counter by one

    Returns:
        A string of the current txtcounter line

    """

    i = read_counter(txtcounter, increment=False)
    logging.info("Reading the next line in the list")
    return list_[i]


def read_counter(txtcounter, increment=False):
    """
    Return the number in a text file. The text file should contain a single line with a single number.

    Args:
        txtcounter: path to text file.
        increment: If true then increase the number by one

    Returns:
        the integer located in the text file
    """

    logging.info(f"Getting the number from {txtcounter}")
    with open(txtcounter) as tc:
            i = tc.readline()
            if "\n" in i:
                logging.critical(f"{txtcounter} is not reading a integer!")
                raise TypeError("Cannot convert txtcounter to a int!")
            else:
                try:
                    i = int(i)
                except:
                    text = f"{txtcounter} seems to be of the right form, but we cannot convert it into an int"
                    logging.critical(text)
                    raise TypeError("text")

def save_list_as_text(path, some_list):
    """
    Saves a list as a text file.

    Args:
        path: The path to save the file to
        some_list: The list to save

    Returns: None

    """

    logging.info(f"Writing to {path}")
    with open(path, 'w') as f:
        for item in some_list:
            f.write(f"{item}\n")
    logging.info(f"Finished writing {path}")

def read_text_list(path):
    """
    Read a list from a text file

    Args:
        path:

    Returns:

    """
    logging.info(f"Reading {path} and converting to list.")
    with open(path, 'r') as f:
        list_ = f.readlines()
        list_ = [int(line.strip("\n") for line in list_)]
    return list_

def work_on_batch(batch_name):

    pass
    # Test test_users to make sure all is well
    # Ask if want to continue if tests failed

    # Check to make sure batch exists
    # Read the text list
    # Read the counter

    # Start a timer

    # Download next user in list
    # Save the user

    # See how much time passed. if not enough wait.

    # Download their ratings if succesfully downloaded user
    # Check that the two are consistent
    # Save the user ratings

    # See how much time passed and wait

    # Download user shelve info???

    # See how much time passed and wait

    # Increment counter
    # Keep doing this until

def download_user(id, key=KEY):
    """
    Download a user
    Args:
        id: The Goodreads id of the user
        key: Goodreads api developer key

    Returns:

    """

    # Download the user
    # Keep trying and log errors
    # Add failed users to the failed users list
    # Return the user's xml as user_info_id{id}.xml
    pass

def download_user_ratings(id):

    pass

    # Figure out how many books they have
    # Download the rating data
    # Log an error if data mismatch and put in mismatch list
    # Save the xml as user_ratings_id{id}.xml

def download_user_shelves(id):

    pass

    # Get the shelves of each user
    # Cross check with rating data


def save_xml(filename):
    pass

if __name__ == '__main__':
    ready_new_batch(10, "test_batch")


