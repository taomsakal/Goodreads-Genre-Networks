import shelve
import networkx as nx
from networkx.algorithms import bipartite
import sys
from crawler.general import *
import pickle
import os
import community
from collections import Counter
sys.path.append('../')


def make_user_book_dict(user_list):
    """ Assigns a user ID corresponding to index in user_list to a user's list of book objects. """
    return {i: user_list[i] for i in range(len(user_list))}


def create_bipartite_graph(user_list):
    """ Given a list of user objects (each user with a list of book objects),
    this function will construct a bipartite graph of users and books. """
    b_graph = nx.Graph()
    b_graph.add_nodes_from(range(len(user_list)), bipartite=0)
    for i in range(len(user_list)):
        book_list = user_list[i].userbooks
        b_graph.add_edges_from(zip([i] * len(book_list), [book.title for book in book_list]))
    for node in b_graph.nodes():
        if 'bipartite' not in b_graph.node[node]:
            b_graph.node[node]['bipartite'] = 1
    return b_graph


def find_weights(book_pair_weights, b_graph, user_dict, users, edge_scheme):
    """ Returns a dictionary mapping book-title pairs to edge weights.
    Argument for edge_scheme is 'min_max' or 'co_rating_len'. """
    # book_pair_weights = {}
    for user in users:
        if edge_scheme == "min_max":
            book_list = [b for b in user_dict[user].userbooks if b.rating > 0]
            for i in range(len(book_list)):
                for j in range(i, len(book_list)):
                    book1 = book_list[i]
                    book2 = book_list[j]
                    if book1.goodreads_id > book2.goodreads_id:
                        book1, book2 = book2, book1
                    if (book1.title, book2.title) in book_pair_weights:
                        book_pair_weights[(book1.title, book2.title)] += [min_max_ratio(book1.rating, book2.rating)]
                    else:
                        book_pair_weights[(book1.title, book2.title)] = [min_max_ratio(book1.rating, book2.rating)]
                    print(book_pair_weights)
            book_pair_weights = {p: sum(book_pair_weights[p]) / len(book_pair_weights[p]) for p in book_pair_weights}
        elif edge_scheme == "co_rating_len":
            book_list = [b for b in user_dict[user].userbooks]
            for i in range(len(book_list)):
                for j in range(i, len(book_list)):
                    book1 = book_list[i]
                    book2 = book_list[j]
                    if book1.goodreads_id > book2.goodreads_id:
                        book1, book2 = book2, book1
                    if (book1.title, book2.title) in book_pair_weights:
                        book_pair_weights[(book1.title, book2.title)] += 1
                    else:
                        book_pair_weights[(book1.title, book2.title)] = 1
        else:
            raise ValueError("Invalid Argument for edge_scheme:%s" % edge_scheme)
    return book_pair_weights


def find_weights_co_rating(book_pair_weights, b_graph, user_dict, users):
    for user in users:
        book_list = [b for b in user_dict[user].userbooks]
        for i in range(len(book_list)):
            for j in range(i, len(book_list)):
                book1 = book_list[i]
                book2 = book_list[j]
                if book1.goodreads_id > book2.goodreads_id:
                    book1, book2 = book2, book1
                pair = (book1.title + "__" + str(book1.goodreads_id), book2.title + "__" + str(book2.goodreads_id))
                if pair in book_pair_weights:
                    book_pair_weights[pair] += 1
                else:
                    book_pair_weights[pair] = 1
    return book_pair_weights


def min_max_ratio(r1, r2):
    return min(r1, r2) / max(r1, r2)


def create_and_save_bipartite():
    """
    This creates a the main book/reader network and saves it as a weighted dict.
    """

    # Decide what data we process
    path = "../data/userlists/"
    file_list = os.listdir(path)
    file_list = file_list[4:60]   # Change this to change amount of data.

    weights_dict = {}
    i = 0
    for file_name in file_list:
        u_list = read(path + file_name)
        u_list_books = [u for u in u_list if len(u.userbooks) > 0]
        bi_graph = create_bipartite_graph(u_list_books)
        user_dict = make_user_book_dict(u_list_books)
        users, books = bipartite.sets(bi_graph)
        weights_dict = find_weights_co_rating(weights_dict, bi_graph, user_dict, users)
        # Print progress
        i += 1
        print("Progress: {}/{}".format(i, len(file_list)))
    with open('weights_dict_co_rating.pickle', 'wb') as f:
        print("Saving weights_dict...")
        pickle.dump(weights_dict, f, protocol=2)

# --------------------------------------

def project_graph(book_weights_dict):
    """
    Create the projected graph, with weights.
    :param book_weights_dict: the weights dictionary
    :return:
    """
    max_ = len(book_weights_dict)
    i = 0
    proj_graph = nx.Graph()
    for pair in book_weights_dict:
        print("Projecting Graph {}/{}".format(i, max_))
        i += 1
        proj_graph.add_edge(*pair, weight=book_weights_dict[pair])

    overwrite(proj_graph, "projection_graph.pickle")

    return proj_graph


def invert_dictionary(clusterDict):
    """Given a dictionary mapping sentences to cluster number, returns
    a dictionary mapping cluster number to a list of book titles in the cluster."""
    invertDict = {}
    for v in clusterDict.values():
        invertDict[v] = []
    for book in clusterDict:
        invertDict[clusterDict[book]].append(book)
    return invertDict


def make_partitions():
    """
    Find the communities in the network
    :return:
    """
    print("Opening the weights dictionary")
    with open('weights_dict_co_rating.pickle', 'rb') as f:
        weights_dict = pickle.load(f)

    # Filter out weak links
    print("Filtering Links...")
    weights_dict = {pair: weights_dict[pair] for pair in weights_dict if weights_dict[pair] > 5}

    print("Projecting Graph")
    proj_graph = project_graph(weights_dict)

    print("Generating Partition Dendogram")
    partition_dendogram = community.generate_dendrogram(proj_graph)

    # print("Inverting dictionary")
    # clusters = invert_dictionary(partition_dendogram)

    # print("Filtering Clusters")
    # clusters_filter = {c: clusters[c] for c in clusters if len(clusters[c]) > 100}

    with open('partition_dendogram.pickle', 'wb') as f:
        pickle.dump(partition_dendogram, f, protocol=2)
    # with open('clusters.pickle', 'wb') as f:
    #     pickle.dump(clusters, f, protocol=2)

# --------------------------------

def find_genre_distribution():
    sys.path.append("../")

    # Open the data
    s = shelve.open('../data/book_db/amazon_bookshelf.db')
    with open('clusters.pickle', 'rb') as f:
        clusters = pickle.load(f)

    genre_clusters = {c: [] for c in clusters}
    for c in clusters:
        book_list = clusters[c]
        for book_info in book_list:
            goodreads_id = book_info.split("__")[1]  # string
            if goodreads_id in s and s[goodreads_id] != "Skipped":
                genre_clusters[c].extend(s[goodreads_id].genres)

    genre_distribution = {c: Counter(genre_clusters[c]) for c in genre_clusters}

    with open('genre_distribution.pickle', 'wb') as f:
        pickle.dump(genre_distribution, f, protocol=2)


def make_graphs():
    """
    This is the main function. It makes and saves the bipartite graph, the partitions, and the genre distribution.
    :return: none
    """

    create_and_save_bipartite()
    make_partitions()
    # find_genre_distribution()

# ===================================================

if __name__ == "__main__":

    make_graphs()
