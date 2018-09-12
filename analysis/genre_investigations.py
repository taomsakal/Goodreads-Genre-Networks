"""
Remember the dendogram is a list of dictionaries. The first dictionary maps books to the lowest level of partitions.
Each successive dictionary maps each level of partitions to a higher one.
"""

import shelve
import sys
import networkx as nx

import pickle
from community import *
import ast

import matplotlib.pyplot as plt
import numpy as np
# import plotly.plotly as py

import collections




# Create global data sources
# -------------------------------------


def build_projection_and_distribution(projection_type):
    """
    Builds the projection data and finds the distributions.
    :param projection_type: "Count", "Overlap" or "Collaboration"
    :return:
    """

    sys.path.append("../")

    PARTITION_TYPE = projection_type

    # The amazon bookshelf
    s = shelve.open('../data/book_db/amazon_bookshelf.db')

    # partitions is the partition dictionary we get from community.best_partition
    with open('partition_dendogram.pickle', 'rb') as f:
        dendogram = pickle.load(f)

    # This is the projected graph
    with open('projection_graph_{}_labeled.pickle'.format(PARTITION_TYPE), 'rb') as f:
        G = pickle.load(f)

    # Find and save the distribution.
    dist = find_distribution(G)
    with open('partition_dendogram.pickle', 'wb') as f:
        pickle.dump("distribution_{}".format(PARTITION_TYPE), f, protocol=2)


    # for i in range(0, len(dist[1])):
    #     try:
    #         data = dist[1][i]
    #         make_plot(data, cutoff=5)
    #         plt.savefig('Figures/fig_{}.png'.format(i), bbox_inches='tight')
    #     except:
    #         pass





def make_lookup_dict(G):
    """
    Make a dictionary of the form {node_name: node num, ... } to allow us to pick and choose a node in the graph.
    :param G: A graph G
    :return: The lookup dict
    """
    lookup_dict = {}
    for i in range(0, len(G)):
        lookup_dict[G.nodes()[i]] = i

    return lookup_dict


def node_num(node_name, lookup_dict):
    """
    Takes the node name and does a reverse lookup to get the index of the node.
    :return: Node index integer
    """

    return lookup_dict[node_name]


def dendogram_info(G, dendogram):
    """
    Get info about the dendogram.
    :param dendogram: The dendogram generated from the louvain community algorithm
    :return: none
    """

    # Print number of communities in each level.
    print("We have {} levels of communities in the projection graph\n".format(len(dendogram)))
    for level in range(len(dendogram)):
        i_graph = induced_graph(partition_at_level(dendogram, level), G)
        print("Level {} has {} communities.".format(level, len(i_graph)))
        print("Level {} has a modularity score of {}"
              .format(level, modularity(partition_at_level(dendogram, level), G)))


def print_graph_info(graph):
    """
    Prints the info for the partition graph.
    :param graph: a networkx graph
    :return: None, prints out some info
    """

    print("The graph is of type {}".format(type(graph)))
    print("The graph has {} nodes".format(graph.number_of_nodes()))
    print("The graph has {} edges.".format(graph.number_of_edges()))
    print("The first node is {} and is of type {}".format(graph.nodes(data=True)[0], type(graph.nodes()[0])))


def label_graph(G, dendogram, edge_filter_threshold=0):
    """
    Adds attributes to each nodes showing which cluster they are in, where clusters are numbered.
    Ex: a node may have "Level 0: 13, Level 1: 134, Level 2: 82" as attributes.
    :param G: A network x graph
    :param dendogram: A partition dendogram corresponding to the graph G
    :param edge_filter_threshold: If the weight of the edge is less than this, remove the edge.
    :return: G with the added attributes.
    """
    print("\nLabeling Partitions")
    print("Making lookup dictionary")
    lookup_dict = make_lookup_dict(G)

    print("Base case")
    # Base Case
    # Create an attribute dictionary and then add it to the graph.
    attribute_dict = {}  # a dict of "node index: attribute value" to add
    for book in dendogram[0]:
        # print(book)
        node_index = G.nodes()[node_num(book, lookup_dict)]
        attribute_dict[node_index] = dendogram[0][book]
    nx.set_node_attributes(G, "Level_0", attribute_dict)

    print("Induction Case")
    # Induction Case
    for i in range(1, len(dendogram)):
        print("Iteration {}".format(i))
        attribute_dict = {}
        n_num = nx.number_of_nodes(G)
        j = 0
        for node_index in range(n_num):
            print("Iteration {}: {}/{}".format(i, j, n_num))
            j += 1
            node = G.nodes(data=True)[node_index]
            attribute_dict[G.nodes()[node_index]] = dendogram[i][node[1]["Level_{}".format(i - 1)]]
        nx.set_node_attributes(G, "Level_{}".format(i), attribute_dict)

    # Filter away weak edges
    print("Filtering Edges...")
    for edge in G.edges(data=True):
        if edge[-1]['weight'] < edge_filter_threshold:
            G.remove_edge(edge[0], edge[1])  # remember: edges are tuples of the form (node1, node2, data)

    # Remove isolates created by filtering
    print("Removing isolates...")
    G.remove_nodes_from(nx.isolates(G))

    return G


# --------------------

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

def count_levels(G):
    """
    Counts the levels of communities in a graph G, where the communities are of the form
    data = {'Level_0': 3, 'Level_1': 24, ...}
    :param G: A networkx graph with 'Level_n" attributes
    :return: The number 'Level_n" attributes go up to
    """

    n = G.nodes(data=True)[0]  # Get a node

    i = -1
    while 'Level_{}'.format(i+1) in n[1].keys():
        i += 1

    return i

def find_distribution(G):
    """
    This finds the distribution of genres within communities.
    We make list with an entry for each level
    [Level_0, Level_1, ..., Level_n]
    where each level is a dict of the partitions in the level
    where each partition is a dictionary of genres with the total number of times they are in the partition.

    :param G:
    :return:
    """

    num_levels = count_levels(G)

    level_list = []
    # Make the levels
    for level in range(0, num_levels):

        # Make the partitions
        partitions = {}
        for node in G.nodes(data=True):
            partition_num = node[1]["Level_{}".format(level)]

            # If not inside, then create dictionary for the partition number
            if partition_num not in partitions.keys():
                partitions[partition_num] = {}

            # Otherwise, add to the number of times the genre has appeared.
            else:
                for genre in ast.literal_eval(node[1]["genres"]):  # literal eval b/c the list was turned into a string
                    if genre in partitions[partition_num]:
                        partitions[partition_num][genre] += 1
                    else:
                        partitions[partition_num][genre] = 1

        level_list.append(partitions)


    return level_list

def make_sorted_tuple_list(dict):
    """
    Orders a dict from highest to lowset value by
    """

    sorted_dict = sorted(list(dict.items()), key=lambda x: x[1], reverse=True)
    return sorted_dict

def plot_tuple_list(tlist, cutoff=None):
    """
    Plots a tuple list.
    :param cutoff: If cuttof is N then only makes the plot to the N'th place.
    If it is None then make the entire plot.
    """

    if cutoff is not None:
        tlist = tlist[:cutoff]

    plt.bar(range(0, len(tlist)), [v[1] for v in tlist], align='center')
    plt.xticks(range(len(tlist)), [v[0] for v in tlist])
    plt.show()



    # plot_url = py.plot_mpl(histogram, filename='docs/histogram-mpl-same')

def make_plot(dict, cutoff=None):
    """
    Make a plot from a dict distribution.
    :param dict: The dict to plot
    :param cutoff: If cuttof is N then only makes the plot to the N'th place. Otherwise make all.
    :return: None
    """

    tlist = make_sorted_tuple_list(dict)
    plot_tuple_list(tlist, cutoff=cutoff)






# # reviews=str(abook.reviews),
# # nodes=abook.browse_nodes,
# asin=abook.asin,
# languages=str(abook.languages),
# authors=gbook.authors,
# average_rating=gbook.average_rating,
# description=gbook.description,
# format=gbook.format,
# is_ebook=gbook.is_ebook,
# language_code=gbook.language_code,
# num_pages=gbook.num_pages,
# series_works=gbook.series_works,
# ratings_count=gbook.ratings_count,
# rating_dist=gbook.rating_dist,
# publication_date=gbook.publication_date,
# popular_shelves=gbook.popular_shelves,
