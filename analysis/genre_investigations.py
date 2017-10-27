import shelve
import sys

import pickle
from community import *

# Create global data sources
# -------------------------------------

sys.path.append("../")

# The amazon bookshelf
s = shelve.open('../data/book_db/amazon_bookshelf.db')

# partitions is the partition dictionary we get from community.best_partition
with open('partition_dendogram.pickle', 'rb') as f:
    dendogram = pickle.load(f)

# This is the projected graph
with open('projection_graph.pickle', 'rb') as f:
    projection_graph = pickle.load(f)

def dendogram_info(dendogram):
    """
    Get info about the dendogram.
    :param dendogram: The dendogram generated from the louvain community algorithm
    :return: none
    """

    print("We have {} levels of communities in the projection graph\n".format(len(dendogram)))
    for level in range(len(dendogram)):
        # Print number of communities in each level.
        i_graph = induced_graph(partition_at_level(dendogram, level), projection_graph)
        print("Level {} has {} communities.".format(level, len(i_graph)))
        print("Level {} has a modularity score of {} ."
              .format(level, modularity(partition_at_level(dendogram, level), projection_graph)))
    print("")


def print_graph_info(graph):
    """
    Prints the info for the partition graph.
    :param graph:
    :return:
    """

    print("The graph is of type {}".format(type(graph)))
    print("The graph has {} nodes".format(graph.number_of_nodes()))
    print("The graph has {} edges.".format(graph.number_of_edges()))
    print("The first node is {}.".format(graph.nodes()[0]))

if __name__ == "__main__":

    print_graph_info(projection_graph)
    dendogram_info(dendogram)


    # modularity = community.modularity(partition_dendogram, graph)
    # print(modularity)















