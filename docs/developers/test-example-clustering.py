# test-example-clustering.py

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from segments import *
from map_drawing import *
from clustering import *

# Define a box around Delta de l'Ebre and get the segments
P1 = Point(40.5363713, 0.5739316671)
P2 =Point(40.79886535, 0.9021482)
BOX_EBRE_FLOATS = Box(P1, P2)
segments = get_segments("data/test_datafile_delta_1.dat", BOX_EBRE_FLOATS)

# Execute a clustering
centroid_labels, centroid_coords, edges, new_segments = cluster(segments, 100)

print(centroid_labels)          # an array of numbers (between 0 and 99)
print(centroid_coords)          # list of (100) points
print(max(centroid_labels))     # 99
print(min(centroid_labels))     # 0
print(len(centroid_coords))     # 100

# Export a map from the clustering
export_png_map("output/map_delta_clustered.png", (new_segments, centroid_coords))