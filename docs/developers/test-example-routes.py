# test-example-routes.py

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from segments import *
from map_drawing import *
from graphmaker import *
from monuments import Monument
from routes import _create_tree

# Define a box around Delta de l'Ebre and get the segments
P1 = Point(40.5363713, 0.5739316671)
P2 =Point(40.79886535, 0.9021482)
BOX_EBRE_FLOATS = Box(P1, P2)
segments = get_segments("data/test_datafile_delta_1.dat", BOX_EBRE_FLOATS)

# Create a graph from the segments
G = make_graph(segments)

# Define some monuments
testing_monuments = [   
        Monument("Deltebre", "test", Point(40.72082, 0.71721)),
        Monument("Mirador del Zigurat", "test", Point(40.72304, 0.85995)),
        Monument("Amposta", "test", Point(40.70718, 0.57895))
    ]

# Generate the route tree
start = Point(40.75718, 0.70385)
T = _create_tree(G, start, testing_monuments)

# Export a map from the tree
export_png_map("output/map_delta_routes.png", T)