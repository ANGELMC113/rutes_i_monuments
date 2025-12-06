# tutorial2.py

"""
Programa per mapejar una zona al voltant de Tossa de Mar,
fent cada pas per separat.
"""

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from rutes_i_monuments import *

# Definim la caixa
box_tossa = Box(Point(41.7128, 2.9159), Point(41.7300, 2.9416))

# Veiem l'àrea definida
preview_box("output/preview-tossa.png", box_tossa)

# Definim els segments
segments_tossa = get_segments("data/tossa.dat", box_tossa)

# Veiem els camins en brut
export_png_map("output/segments_tossa.png", segments_tossa)

# Definim el graf
graf_tossa = make_graph(segments_tossa)

# Veiem el mapa del graf
export_png_map("output/graf_tossa.png", graf_tossa)

# Reduïm el mapa a les rutes a monuments, des d'un punt donat a prop de la platja de Tossa
routes_tossa = find_routes(graf_tossa, box_tossa, (Point(41.7202, 2.9335)))

# Visualitzem les rutes
export_png_map("output/rutes_tossa.png", routes_tossa)

# Generem l'arxiu kml de les rutes per portar a Google Earth
export_kml("output/rutes_tossa.kml", routes_tossa)