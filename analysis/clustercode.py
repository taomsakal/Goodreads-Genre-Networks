"""
This makes the graphs and runs the genre analysis.
Comment out the lines we do not need.
"""

from analysis.genre_investigations import build_projection_and_distribution
from analysis.make_graphs import build_graph, project_graph, create_and_save_bipartite
import time

#First we will only make the bipartite graph, leaving in singletons and everything.
text = input("Shall we make the bipartite graphs? (no/yes)")
if text == 'yes':
    text = input("For all nodes, just a small test graph, or a custom amount? (all/test/custom)")
    if text == 'all':
        create_and_save_bipartite()
    elif text == 'test':
        create_and_save_bipartite(start=0, end=1, save_name="test_bipartite")
    elif text == 'custom':
        start = input("Starting file number (integer between 0 and 371)")
        end = input("Ending file number (integer between 1 and 371)")
        start = int(start)
        end = int(end)
        name = input("What will the <name> of the file be?")
        create_and_save_bipartite(start=start, end=end, save_name=name)

# Next load the biportite graph and project it.
text = input("Project all nodes, test graph, or custom graph? (all/test/custom)")
proj_type = 'Count'
if text == 'all':
    project_graph(method=proj_type)
elif text == 'test':
    project_graph(method=proj_type, bipartite_graph_name="test_bipartite.pickle")
elif text == 'custom':
    name = input("Name of the bipartite graph? (<name>.pickle)")
    project_graph(method=proj_type, bipartite_graph_name=f"{name}.pickle")

# project_graph(method=proj_type, bipartite_graph_name="test_bipartite.pickle")
# Next we must find the genre partitions within the graph
# make_partitions()

#===============================
import shelve
import networkx as nx

from crawler.general import *
import pickle
import os
import community
from collections import Counter
from networkx.algorithms import bipartite
from analysis.genre_investigations import label_graph, dendogram_info


# PATH = 'results'
# SUFFIX = '_small'

def build_graph(projection_type, bipartite_only=True, start=0, end=0):
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

def create_bipartite_graph(user_list, degree_threshold=0, amazon_book_dict=None, save_name="bipartite_reader_network"):
    """
    Given a list of user objects (each user with a list of book objects),
    this function will construct a bipartite graph of users and books.
    :param remove_isolates: If true, delete all isolated nodes.
    :param degree_threshold: Remove nodes with degree below or equal to this threshold.
    Set to negative to not remove nodes.
    """

    print(f"Creating bipartite Graph with threshold {degree_threshold}")

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
                                         salesrank=abook_sales_rank,
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
    print(f"Saving Bipartite Graph as {save_name}.pickle...")
    overwrite(b_graph, f"{save_name}.pickle")
    print("Saving gml version...")
    nx.write_gml(b_graph, f"{save_name}.gml")
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
        try:
            G.remove_nodes_from(nx.isolates(G))
        except:
            print("Could not remove isolated nodes!")
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


def create_and_save_bipartite(degree_threshold=0, start=0, end=0, save_name="bipartite_reader_network"):
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
    print("Collecting Userlists")
    l = len(file_list)
    i = 0
    user_lists = []
    for file_name in file_list:
        user_list = read(path + file_name)
        user_lists += [u for u in user_list if len(u.userbooks) > 0]
        print(f"Userlist {i}/{l} collected.")
        i += 1

    bi_graph = create_bipartite_graph(user_lists, degree_threshold, amazon_book_dict, save_name=save_name)

    return bi_graph


def project_graph(bipartite_graph_name='bipartite_reader_network.pickle', method="Count"):
    """
    Create the projected graph, with weights.
    :param book_weights_dict: the weights dictionary, which is of the form {(title1_gid, title2_gid) : weight, ...}
    :param method: This tells us how to weight the edges. "Rating count" sums all the ratings for a weight.
    "Average" takes the average. "Count" just counts the number of times the edge is shared (co-read).
    :return: A nx graph.
    """

    print("Projecting Graph with {} method.".format(method))
    print(f"Reading {bipartite_graph_name}...")

    bi_graph = read(bipartite_graph_name)

    if not bipartite.is_bipartite(bi_graph):
        raise Exception("Projecting non-bipartite graphs is felony.")

    # Make top nodes (users) to project down onto bottom nodes (books)
    print("Gathering user nodes...")
    top_nodes = {n for n, d in bi_graph.nodes(data=True) if d['bipartite'] == 0}
    print("Gathering book nodes...")
    bottom_nodes = set(bi_graph) - top_nodes

    # Various projection methods
    print(f"Projecting with the {method} method... (This might take a long time.)")
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

    print("Projection succesful!")

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

    print("Dendogram created. Saving...")
    with open('partition_dendogram.pickle', 'wb') as f:
        pickle.dump(partition_dendogram, f, protocol=2)

    print("Done!")

    return G, partition_dendogram


# --------------------------------


# ==========================


