import networkx as nx
import community
import cPickle as pickle

with open('weights_dict_co_rating.pickle', 'rb') as f:
    weights_dict = pickle.load(f)


def project_graph(book_weights_dict):
    proj_graph = nx.Graph()
    for pair in book_weights_dict:
        proj_graph.add_edge(*pair, weight=book_weights_dict[pair])
    return proj_graph


def invertDictionary(clusterDict):
    """Given a dictionary mapping sentences to cluster number, returns
    a dictionary mapping cluster number to a list of book titles in the cluster."""
    invertDict = {}
    for v in clusterDict.values():
        invertDict[v] = []
    for book in clusterDict:
        invertDict[clusterDict[book]].append(book)
    return invertDict


weights_dict = {pair: weights_dict[pair] for pair in weights_dict if weights_dict[pair] > 5}

proj_graph = project_graph(weights_dict)
partition = community.best_partition(proj_graph)
clusters = invertDictionary(partition)
clusters_filter = {c: clusters[c] for c in clusters if len(clusters[c]) > 100}

with open('clusters.pickle', 'wb') as f:
    pickle.dump(clusters_filter, f, protocol=2)
