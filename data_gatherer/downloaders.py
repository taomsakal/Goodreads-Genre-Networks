"""
This downloads the user data and user rating data from Goodreads through their api.
It takes a random sample of users form 0 to NUM_USERS

You'll need a developer key to get any data, and permission from Goodreads to store, analyse, and publish the data.
(Please see the Goodreads API terms of use.)


"""

SPEED_LIMIT = 2  # How many seconds to wait before next request. Must be greater than one.
KEY = ''  # The developer key. You'll want to keep this secret.
NUM_USERS = 86737928  # The current number of users on Goodreads. This is accurate to within 1000 as of 9/13/2018

def make_user_list(forbidden_users, start_number=1, max_number=NUM_USERS):
    """
    Makes a list of random users.

    Args:
        forbidden_users: Users that cannot be added.
        start_number:
        max_number:

    Returns:

    """

    # Make the list as a set first
    # Save into a text file.

def ready_new_batch(max_num, folder_name):
    """
    Set up a folder for a new batch of users to be crawled.
    The folder will be located in data/raw/users/<folder name> and it will have three things

    1. A subfolder called "user_ratings_xml" which stores the raw user book list xml files
    2. A subfolder called "users_xml" which stores the raw user information xml files
    3. A list of random users, called "userlist.txt"
    4. A plaintext object called "current_user.txt" that tells us the current user we are on
    5. A plaintext of failed users
    6. A plaintext of users with questionable data

    Args:
        max_num:
        folder_name:

    Returns:

    """

    # Make the files
    # Throw error if file already exists

def read_text_list():
    pass

def save_list_as_text():
    pass

def work_on_batch(batch_name):


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

def download_user_ratings(id):

    # Figure out how many books they have
    # Download the rating data
    # Log an error if data mismatch and put in mismatch list
    # Save the xml as user_ratings_id{id}.xml

def download_user_shelves(id):

    # Get the shelves of each user
    # Cross check with rating data


def save_xml(filename):
    pass



