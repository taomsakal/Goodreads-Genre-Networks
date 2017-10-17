import shelve
import sys

import pickle
import community


sys.path.append("../")

# Open the data
s = shelve.open('../data/book_db/amazon_bookshelf.db')

# partitions is the partition dictionary we get from community.best_partition
with open('partition.pickle', 'rb') as f:
    partitions = pickle.load(f)
# clusters is the partition dictionary inverted.
with open('clusters.pickle', 'rb') as f:
    clusters = pickle.load(f)
# This is a distribution of the genres, according to amazon.
with open('genre_distribution.pickle', 'rb') as f:
    dist = pickle.load(f)
# This is a distribution of the genres, according to amazon.
with open('projection_graph.pickle', 'rb') as f:
    graph = pickle.load(f)


if __name__ == "__main__":

    modularity = community.modularity(partitions, graph)
    print(modularity)

    dendo = community.generate_dendrogram(graph)
    for level in range(len(dendo) - 1):
        print("partition at level", level, "is", community.partition_at_level(dendo, level))




