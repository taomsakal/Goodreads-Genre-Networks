"""
Remember the dendogram is a list of dictionaries. The first dictionary maps books to the lowest level of partitions.
Each successive dictionary maps each level of partitions to a higher one.
"""

import shelve
import sys
import networkx as nx

import pickle
from community import *

# Create global data sources
# -------------------------------------

sys.path.append("../")


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
    print("Labeling Partitions")
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
        for node_index in range(nx.number_of_nodes(G)):
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

# Todo
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


if __name__ == "__main__":
    # The amazon bookshelf
    #  s = shelve.open('../data/book_db/amazon_bookshelf.db')

    # partitions is the partition dictionary we get from community.best_partition
    with open('partition_dendogram.pickle', 'rb') as f:
        dendogram = pickle.load(f)

    print(dendogram[1])

    # # This is the projected graph
    # with open('projection_graph.pickle', 'rb') as f:
    #     projection_graph = pickle.load(f)
    #
    #
    #
    # print_graph_info(projection_graph)
    # #dendogram_info(dendogram)
    # label_graph(projection_graph, dendogram)
    #

    # modularity = community.modularity(partition_dendogram, graph)
    # print(modularity)






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
