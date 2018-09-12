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
    name = input("What will the <name> of the file be?")
    threshold = input("What will the degree threshold be?")
    create_and_save_bipartite(name, degree_threshold=int(threshold))

# Next load the biportite graph and project it.
name = input("<name>.pickle of the graph to project?")
proj_type = input("What type of projection? Overlap (1) / Weighted (2) / Rachel's (3)")
if proj_type == '1':
    project_graph(method='Overlap', bipartite_graph_name=f"{name}.pickle")
if proj_type == '2':
    project_graph(method='Weighted', bipartite_graph_name=f"{name}.pickle")
# project_graph(method=proj_type, bipartite_graph_name="test_bipartite.pickle")
# Next we must find the genre partitions within the graph
# make_partitions() # Finally we must