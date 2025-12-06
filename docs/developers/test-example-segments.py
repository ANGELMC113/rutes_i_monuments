# test-example-segments.py

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from segments import *
from map_drawing import *

# Define a box around Delta de l'Ebre
P1 = Point(40.5363713, 0.5739316671)
P2 =Point(40.79886535, 0.9021482)
BOX_EBRE_FLOATS = Box(P1, P2)

# Download the segments
segments = get_segments("data/test_datafile_delta_1.dat", BOX_EBRE_FLOATS)

# Export a map from the segments
export_png_map("output/map_delta_segments.png", segments)