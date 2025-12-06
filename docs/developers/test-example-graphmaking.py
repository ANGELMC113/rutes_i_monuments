# test-example-graphmaking.py

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from segments import *
from map_drawing import *
from graphmaker import *

# Define a box around Delta de l'Ebre and get the segments
P1 = Point(40.5363713, 0.5739316671)
P2 =Point(40.79886535, 0.9021482)
BOX_EBRE_FLOATS = Box(P1, P2)
segments = get_segments("data/test_datafile_delta_1.dat", BOX_EBRE_FLOATS)

# Create a graph from the segments
G = make_graph(segments)

print(G)                # Graph with 100 nodes and 220 edges
print(G.edges)          # list[tuple[int, int]]
print(G.nodes.data())   # list[tuple[int, dict['Point': Point]]]
print(G.edges.data())   # list[tuple[int, int, dict['distance': float]]]

# Export a map from the graph
export_png_map("output/map_delta_graf.png", G)

# Export a KML from the graph
export_kml("output/map_delta_graf.kml", G)