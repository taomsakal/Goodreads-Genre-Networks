"""
This makes the graphs and runs the genre analysis.
"""

from analysis.genre_investigations import build_projection_and_distribution
from analysis.make_graphs import build_graph

proj_type = "Count"
build_graph(proj_type, start=10, end=13)
build_projection_and_distribution(proj_type)
