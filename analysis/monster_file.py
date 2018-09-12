#! /home/taomsakal/anaconda3/bin/python
#PBS -l nodes=1:ppn=12
#PBS -l walltime=1:00:00
#PBS -V
# -*- coding: utf-8 -*-

"""
Sometimes life is hard and importing modules doesn't work.
This file has everything needed for the analysis. It is just a copy-paste of everything in
make_graphs.py
genre_investigations.py
general.py

"""

import shelve
import networkx as nx

import pickle
import os
from community import *
from collections import Counter
from networkx.algorithms import bipartite



# =========================


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


# ============================



def build_graph(projection_type, start=0, end=0):
    """
    Builds the graph.
    :param projection_type: "Count", "Overlap" or "Collaboration"
    :return: None
    """

    sys.path.append('../')

    name = "projection_graph_{}".format(projection_type)

    make_graphs(method="Collaboration", start=start, end=end)
    G, dendogram = make_partitions(name="{}.pickle".format(name))
    dendogram_info(G, dendogram)
    G = label_graph(G, dendogram, edge_filter_threshold=2)

    # Save the graph
    print("Saving Labeled Graph as {}_labeled.pickle...".format(name))
    overwrite(G, "{}_labeled.pickle...".format(name))
    print("Saving Labeled Graph as {}_labeled.gml...".format(name))
    nx.write_gml(G, "{}_labeled.gml".format(name))

    print("FINISHED BUILDING GRAPHS.")

def create_bipartite_graph(user_list, degree_threshold=0, amazon_book_dict=None):
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
                        try:
                            abook_genres = str(amazon_book_dict[
                                                   str(book.goodreads_id)].genres)  # not all books are in amazon
                            abook_sales_rank = int(amazon_book_dict[str(book.goodreads_id)].sales_rank)
                        except:
                            abook_genres = "[\"Not in Amazon Database\"]"
                            abook_sales_rank = -1  # Negative one sales rank if not in database
                            # print("{} is not in our Amazon database.".format(book.title))
                        b_graph.add_node("book_{}".format(book.goodreads_id),
                                         bipartite=1,
                                         gid=book.goodreads_id,
                                         title=book.title,
                                         sales_rank=abook_sales_rank,
                                         genres=abook_genres
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

    # Clean the Graph of broken bipartite values (Which get added for a ~5% of books when getting amazon data)

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


def create_and_save_bipartite(degree_threshold=0, start=0, end=0):
    """
    This creates a the main book/reader network and saves it as a pickle and a gml file.
    :param start: Where to start processing in the data file list
    :param end:  Where to end processing in the data file list. If 0 then we process all the data.
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
    if end != 0:
        file_list = file_list[start:end]


    # Collect userlists and make a bipartite graph from them
    user_lists = []
    for file_name in file_list:
        user_list = read(path + file_name)
        user_lists += [u for u in user_list if len(u.userbooks) > 0]

    bi_graph = create_bipartite_graph(user_lists, degree_threshold, amazon_book_dict)

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
    elif method == "Average Weight": # todo
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    elif method == "Divergence": # todo
        proj_graph = bipartite.collaboration_weighted_projected_graph(bi_graph, bottom_nodes)
    else:
        raise Exception("{} is not a valid projection method".format(method))

    # Save
    print("Saving projection_graph_{}.pickle".format(method))
    overwrite(proj_graph, "projection_graph_{}.pickle".format(method))
    print("Saving projection_graph_{}.gml".format(method))
    nx.write_gml(proj_graph, "projection_graph_{}.gml".format(method))

    return proj_graph


def make_graphs(method="Count", start=0, end=0):
    """
    This is the main function. It makes and saves the bipartite graph, the partitions, and the genre distribution.
    :return: none
    """

    create_and_save_bipartite(degree_threshold=1, start=start, end=end)
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

    print("Generating Partition Dendogram")
    partition_dendogram = community.generate_dendrogram(G)

    with open('partition_dendogram.pickle', 'wb') as f:
        pickle.dump(partition_dendogram, f, protocol=2)

    return G, partition_dendogram


# --------------------------------


# ==========================


import pickle

import pandas


"""
The code below prevents a unpickling error
"""
import sys
import pandas.core.indexes
sys.modules['pandas.indexes'] = pandas.core.indexes
import pandas.core.base, pandas.core.indexes.frozen
setattr(sys.modules['pandas.core.base'],'FrozenNDArray', pandas.core.indexes.frozen.FrozenNDArray)



def print_(string, print_status=True):
    """
    Print the string if get_status is true
    :param string: string to print
    :return: None
    """

    if print_status:
        print(string)


def print_full(x):
    """
    Prints the full dataframe.
    """
    pandas.set_option('display.max_rows', len(x))
    print(x)
    pandas.reset_option('display.max_rows')


def overwrite(data, filename):
    """
    Saves the data to a file, overwriting previous data.
    """

    file = open(filename, "wb")
    pickle.dump(data, file)
    file.close()


def read(filename):
    """
    Read data from a file.
    :return: data in file
    """

    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()

    return data

# ==============================



if __name__ == "__main__":


  print_file = open("log.txt", "a")

  startime = time.time()
  print("Started at {}".format(startime), file=print_file)

  proj_type = "Count"
  print("Projection Type is {}".format(proj_type), file=print_file)

  #build_graph(proj_type, start=10, end=12)
  print("Finished Building graph at time {} and it took {}.".format(time.time(), time.time() - startime), file=print_file)
  build_time = time.time()

  #build_projection_and_distribution(proj_type)
  print("Finished Building graph at time {} and it took {}.".format(time.time(), time.time() - build_time), file=print_file)

  print("The entire process took {}.".format(time.time() - startime), file=print_file)


