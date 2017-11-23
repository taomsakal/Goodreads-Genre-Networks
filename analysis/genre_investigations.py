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


def dendogram_info(dendogram):
    """
    Get info about the dendogram.
    :param dendogram: The dendogram generated from the louvain community algorithm
    :return: none
    """

    # Print number of communities in each level.
    print("We have {} levels of communities in the projection graph\n".format(len(dendogram)))
    for level in range(len(dendogram)):
        i_graph = induced_graph(partition_at_level(dendogram, level), projection_graph)
        print("Level {} has {} communities.".format(level, len(i_graph)))
        print("Level {} has a modularity score of {} ."
              .format(level, modularity(partition_at_level(dendogram, level), projection_graph)))



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

def label_graph(G, dendogram):
    """
    Adds attributes to each nodes showing which cluster they are in, where clusters are numbered.
    Ex: a node may have "Level 0: 13, Level 1: 134, Level 2: 82" as attributes.
    :param G: A network x graph
    :param dendogram: A partition dendogram corresponding to the graph G
    :return: G with the added attributes.
    """


    lookup_dict = make_lookup_dict(G)

    # Base Case
    attribute_dict = {}  # a dict of "node index: attribute value" to add
    for book in dendogram[0]:
        print(book)
        node_index = projection_graph.nodes()[node_num(book, lookup_dict)]
        attribute_dict[node_index] = dendogram[0][book]
    nx.set_node_attributes(G, "Level 0", attribute_dict)


    # # Base Case
    # nx.set_node_attributes(projection_graph, "Level 0", "Null")
    # for node in projection_graph.nodes():
    #     partition_num = dendogram[0][node]
    #     print(projection_graph.nodes(data=True)[node_num(node, lookup_dict)])# = partition_num
    #
    print(nx.get_node_attributes(projection_graph, "Level 0"))




        # i_graph = induced_graph(partition_at_level(dendogram, level), projection_graph)
        # print("Level {} has {} communities.".format(level, len(i_graph)))
        # print("Level {} has a modularity score of {} ."
        #       .format(level, modularity(partition_at_level(dendogram, level), projection_graph)))




if __name__ == "__main__":

    # The amazon bookshelf
   #  s = shelve.open('../data/book_db/amazon_bookshelf.db')

    # partitions is the partition dictionary we get from community.best_partition
    with open('partition_dendogram.pickle', 'rb') as f:
        dendogram = pickle.load(f)

    # This is the projected graph
    with open('projection_graph.pickle', 'rb') as f:
        projection_graph = pickle.load(f)



    print_graph_info(projection_graph)
    #dendogram_info(dendogram)
    label_graph(projection_graph, dendogram)


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








