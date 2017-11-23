import shelve
import networkx as nx
from networkx.algorithms import bipartite
import sys
from crawler.general import *
import pickle
import os
import community
from collections import Counter
from networkx.algorithms import bipartite

sys.path.append('../')


def create_bipartite_graph(user_list, degree_threshold=0):
    """
    Given a list of user objects (each user with a list of book objects),
    this function will construct a bipartite graph of users and books.
    :param remove_isolates: If true, delete all isolated nodes.
    :param degree_threshold: Remove nodes with degree below or equal to this threshold.
    Set to negative to not remove nodes.
    """

    b_graph = nx.Graph()

    # Make the Nodes and edges
    # IMPORTANT: Give each user an id of i instead of their original id. We do this because some early users
    # have an id of 0 due to a bug.
    max_ = len(user_list)
    i = 0
    for user in user_list:
        if user.profile_type == "normal":
            b_graph.add_node("user_{}".format(i), bipartite=0)
            for book in user.userbooks:
                try:
                    if book.goodreads_id != "No gid":
                        # abook = amazon_book_dict[str(book.goodreads_id)]  # not all books are in amazon
                        # gbook = book_dict[str(book.goodreads_id)][1]
                        b_graph.add_node("book_{}".format(book.goodreads_id),
                                         bipartite=1,
                                         gid=book.goodreads_id,
                                         title=book.title,
                                         # sales_rank=int(abook.sales_rank),
                                         # genres=str(abook.genres),

                                         )
                except:
                    pass
                # print("Skipped {}.".format(book.title))

                # Add the edges if weight is not zero
                if book.rating != 0:
                    b_graph.add_edge("user_{}".format(i), "book_{}".format(book.goodreads_id),
                                     weight=book.rating,
                                     rating=book.rating,
                                     readcount=book.readcount)

        i += 1
        print("Building Bipartite Graph: {}/{}".format(i, max_))

    b_graph = remove_nodes_below_threshold(b_graph, degree_threshold)

    # Save the graph
    print("Saving Bipartite Graph as bipartite_reader_network.pickle...")
    overwrite(b_graph, "bipartite_reader_network.pickle")
    print("Saving Bipartite Graph as bipartite_reader_network.gml...")
    nx.write_gml(b_graph, "bipartite_reader_network.gml")
    print("Save Successful!")

    return b_graph

def remove_nodes_below_threshold(G, degree_threshold=1):
    """
    Remove the nodes with degree below the threshold.
    :param G: A graph
    :param degree_threshold: Remove nodes with degree less than this. Put at 0 to not run this
    :return:
    """

    # Remove isolate case. This does work.
    if degree_threshold == 1:
        G.remove_nodes_from(nx.isolates(G))

    # More general version. Does not work right now.
    # if degree_threshold > 0:
    #     print("Removing Nodes with degree less than or equal to {}".format(degree_threshold))
    #     removal_list = []
    #     for node in G.nodes():
    #         if nx.degree(G, node) < degree_threshold:
    #             removal_list.append(node)
    #             print(node)
    #
    #     print(removal_list)
    #     G.remove_nodes_from(removal_list)

    return G

def create_and_save_bipartite(degree_threshold=0):
    """
    This creates a the main book/reader network and saves it as a pickle and a gml file.
    :param degree_threshold: Remove nodes with degree below or equal to this threshold.
    Set to negative to not remove nodes.
    """

    print("Opening Goodreads book dict")
    goodreads_book_dict = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')
    print("Opening Amazon book dict")
    amazon_book_dict = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')

    # Decide what data we process
    path = "../data/userlists/"
    file_list = os.listdir(path)
    file_list = file_list[10:20]  # Change this to change amount of data.

    # Collect userlists and make a bipartite graph from them
    user_lists = []
    for file_name in file_list:
        user_list = read(path + file_name)
        user_lists += [u for u in user_list if len(u.userbooks) > 0]

    bi_graph = create_bipartite_graph(user_lists, degree_threshold)

    return bi_graph


def project_graph(name='bipartite_reader_network.pickle', method="Count"):
    """
    Create the projected graph, with weights.
    :param book_weights_dict: the weights dictionary, which is of the form {(title1_gid, title2_gid) : weight, ...}
    :param method: This tells us how to weight the edges. "Rating count" sums all the ratings for a weight.
    "Average" takes the average. "Count" just counts the number of times the edge is shared (co-read).
    :return: A nx graph.
    """

    print("Projecting Graph with {} method.".format(method))

    bi_graph = read(name)

    if not bipartite.is_bipartite(bi_graph):
        raise Exception("Projecting non-bipartite graphs is felony.")

    # Make top nodes (users) to project down onto bottom nodes (books)
    top_nodes = {n for n, d in bi_graph.nodes(data=True) if d['bipartite'] == 0}
    bottom_nodes = set(bi_graph) - top_nodes

    # Various projection methods
    if method == "Count":  # Count the number of co-reads
        proj_graph = bipartite.generic_weighted_projected_graph(bi_graph, bottom_nodes)
    elif method == "Collaboration":  # Newman's collaboration metric
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    elif method == "Overlap":  # Proportion of neighbors that are shared
        proj_graph = bipartite.overlap_weighted_projected_graph(bi_graph, bottom_nodes)
    elif method == "Average Weight":
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    elif method == "Divergence":
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    else:
        raise Exception("{} is not a valid projection method".format(method))

    # Save
    print("Saving projection_graph_{}.pickle".format(method))
    overwrite(proj_graph, "projection_graph_{}.pickle".format(method))
    print("Projection successful.")
    print("Saving projection_graph_{}.gml".format(method))
    nx.write_gml(proj_graph, "projection_graph_{}.gml".format(method))
    print("Save successful.")

    return proj_graph



def make_graphs():
    """
    This is the main function. It makes and saves the bipartite graph, the partitions, and the genre distribution.
    :return: none
    """

    create_and_save_bipartite(degree_threshold=1)
    project_graph(method="Count")
    # make_partitions()
    # find_genre_distribution()


# ===================================================

def make_partitions(name='projection_graph.pickle'):
    """
    Find the communities in the network
    :param name: name of graph pickle file
    :return:
    """

    G = read(name)

    # # Filter out weak links
    # print("Filtering Links...")
    # weights_dict = {pair: weights_dict[pair] for pair in weights_dict if weights_dict[pair] > 5}

    print("Generating Partition Dendogram")
    partition_dendogram = community.generate_dendrogram(G)

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

#==========================


if __name__ == "__main__":
    make_graphs()
    make_partitions(name="projection_graph_Count.pickle")
