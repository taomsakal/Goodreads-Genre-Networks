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


    # Remove nodes with degree below the threshold.
    # Most useful for removing nodes with no edges (these usually are users that rated everything 0)
    if degree_threshold > 0:
        print("Removing Nodes with degree less than or equal to {}".format(degree_threshold))
        for node in b_graph.nodes():
            if node.d
            b_graph.remove_node(node)

    # Save the graph
    print("Saving Bipartite Graph as bipartite_reader_network.pickle...")
    overwrite(b_graph, "bipartite_reader_network.pickle")
    print("Saving Bipartite Graph as bipartite_reader_network.gml...")
    nx.write_gml(b_graph, "bipartite_reader_network.gml")
    print("Save Successful!")

    return b_graph


def create_and_save_bipartite():
    """
    This creates a the main book/reader network and saves it as a weighted dict.
    The dict is of the form { (title1_gid, title2_gid) : weight), ... }
    """

    print("Opening Goodreads book dict")
    goodreads_book_dict = shelve.open("../data/book_db/goodreads_bookshelf.db", flag='r')
    print("Opening Amazon book dict")
    amazon_book_dict = shelve.open("../data/book_db/amazon_bookshelf.db", flag='r')

    # Decide what data we process
    path = "../data/userlists/"
    file_list = os.listdir(path)
    file_list = file_list[10:15]  # Change this to change amount of data.

    # Collect userlists and make a bipartite graph from them
    user_lists = []
    for file_name in file_list:
        user_list = read(path + file_name)
        user_lists += [u for u in user_list if len(u.userbooks) > 0]

    bi_graph = create_bipartite_graph(user_lists, goodreads_book_dict, amazon_book_dict, remove_isolates=True)

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

    #data_dict = make_data_dict(bi_graph)

    # data_dict_to_projection(data_dict, func)
    top_nodes = {n for n, d in bi_graph.nodes(data=True) if d['bipartite'] == 0}
    bottom_nodes = set(bi_graph) - top_nodes
    print(bottom_nodes)
    print("===============")
    print(top_nodes)

    if method == "Count":  # Count the number of co-reads
        proj_graph = bipartite.generic_weighted_projected_graph(bi_graph, bottom_nodes)
    if method == "Collaboration":  # Newman's collaboration metric
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    if method == "Overlap":  # Proportion of neighbors that are shared
        proj_graph = bipartite.overlap_weighted_projected_graph(bi_graph, bottom_nodes)
    if method == "Average Weight":
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    if method == "Divergence":
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    else:
        raise Exception("{} is not a valid projection method".format(method))

    overwrite(proj_graph, "projection_graph.pickle")

    # Save
    print(bi_graph.number_of_edges())
    print("Projection successful.")
    print("Saving projection_graph_{}.gml".format(method))
    nx.write_gml(proj_graph, "projection_graph_{}.gml".format(method))

    return proj_graph

# Don't need this function anymore
def make_data_dict(bi_graph):
    """
    This makes a dictionary of the the form
    {(book1_gid, book2_gid): [(b1_rating, b2_rating, owner_data), .... (b1_rating, b2_rating, owner_data)]}
    We can use this dictionary to make custom weight calculations.
    :param bi_graph: A bipartite graph.
    :return:
    """

    data_dict = {}

    # Seperate the top (top) and bottom (book) nodes. The bottom nodes are the ones we project onto.
    top_nodes = {n for n, d in bi_graph.nodes(data=True) if d['bipartite'] == 0}
    bottom_nodes = set(bi_graph) - top_nodes

    # Connect every neighbor with eachother
    for user in top_nodes:
        neighbors = bi_graph.neighbors(user)
        computed_pairs = {}
        for node in neighbors:
            for node2 in neighbors:

                print(user, node, node2)

                # Decide on canonical order for nodes. The one with the smaller goodreads id comes first
                if node['gid'] > node2['gid']:
                    node, node2 = node2, node
                pair_string = '{},{}'.format(node['gid'], node2['gid'])

                # Check if node-pair is in dictionary
                in_dict = pair_string in computed_pairs.keys()

                # Skip self and already computed pairs
                if node == node2 or in_dict:
                    continue

                # Add to dictionary if not in dict, otherwise update the list
                new_tuple = [(bi_graph.edges[user, node]['weight'], bi_graph.edges[user, node2]['weight'], user.id)]
                if not in_dict:
                    data_dict[pair_string] = [new_tuple]
                else:
                    data_dict[pair_string] += [new_tuple]

    return data_dict

def make_partitions():
    """
    Find the communities in the network
    :return:
    """

    # # Filter out weak links
    # print("Filtering Links...")
    # weights_dict = {pair: weights_dict[pair] for pair in weights_dict if weights_dict[pair] > 5}

    print("Projecting Graph")
    proj_graph = project_graph()

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

    G = create_and_save_bipartite()
    project_graph(method="Overlap")
    # make_partitions()
    # find_genre_distribution()


# ===================================================


if __name__ == "__main__":
    make_graphs()
